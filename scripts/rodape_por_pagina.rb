# frozen_string_literal: true
# =============================================================================
# Extensão Asciidoctor PDF — Notas de rodapé ao pé da página de origem
# Projeto: Relatório de Gestão SETADES (2023–2026)
# =============================================================================
# Por padrão, o Asciidoctor PDF agrupa as notas de rodapé ao final do capítulo.
# Esta extensão intercepta a criação de notas de rodapé, reserva o espaço
# necessário na parte inferior da página atual e as renderiza logo acima do
# rodapé da mesma página onde foram referenciadas.
# =============================================================================

require 'asciidoctor/pdf'

module SetadesPageFootnotes
  FOOTNOTE_RULE_TOP_PADDING = 8
  FOOTNOTE_RULE_BOTTOM_PADDING = 4
  FOOTNOTE_RULE_WIDTH_RATIO = 0.35
  FOOTNOTE_RULE_COLOR = 'CFCFCF'
  FOOTNOTE_SAFETY_PADDING = 4

  def convert_inline_footnote node
    result = super
    return result if scratch? || !defined?(@rendered_footnotes)

    if (index = node.attr 'index') && (fn = node.document.footnotes.find { |c| c.index == index })
      @pending_page_footnotes ||= []
      unless @rendered_footnotes.include?(fn) || @pending_page_footnotes.include?(fn)
        @pending_page_footnotes << fn
        reserve_footnote_space_on_page
      end
    end
    result
  end

  def start_new_page options = {}
    if !scratch? && @pending_page_footnotes && !@pending_page_footnotes.empty? && !@flushing_page_footnotes
      flush_pending_page_footnotes
    end
    super
  end

  def ink_footnotes node
    if !scratch? && @pending_page_footnotes && !@pending_page_footnotes.empty? && !@flushing_page_footnotes
      flush_pending_page_footnotes
    end
    super
  end

  private

  def full_body_width
    page.dimensions[2] - page.margins[:left] - page.margins[:right]
  end

  def measure_pending_footnotes_height(fns)
    return 0 if fns.empty?

    total = FOOTNOTE_RULE_TOP_PADDING + FOOTNOTE_RULE_BOTTOM_PADDING + FOOTNOTE_SAFETY_PADDING
    item_spacing = (@theme.footnotes_item_spacing || 3).to_f
    index_offset = @rendered_footnotes.length
    body_width = full_body_width

    theme_font :footnotes do
      line_metrics = calc_line_metrics(@theme.footnotes_line_height || 1.3)
      fns.each_with_index do |fn, i|
        label = fn.index - index_offset
        formatted = text_formatter.format("[#{label}] #{fn.text}")
        total += height_of_formatted(formatted, width: body_width, leading: line_metrics.leading)
        total += item_spacing if i < fns.length - 1
      end
    end
    total
  end

  def reserve_footnote_space_on_page
    return unless @margin_box

    @footnote_reserved_height ||= 0
    needed = measure_pending_footnotes_height(@pending_page_footnotes)
    delta = needed - @footnote_reserved_height
    return if delta <= 0

    current_height = @margin_box.instance_variable_get(:@height)
    new_abs_bottom = @margin_box.absolute_top - (current_height - delta)
    if y > new_abs_bottom + 4
      @margin_box.instance_variable_set(:@height, current_height - delta)
      @footnote_reserved_height += delta
    end
  end

  def flush_pending_page_footnotes
    fns = @pending_page_footnotes
    return if fns.nil? || fns.empty?

    @flushing_page_footnotes = true
    @pending_page_footnotes = []

    reserved = @footnote_reserved_height || 0
    @footnote_reserved_height = 0

    if @margin_box && reserved > 0
      current_height = @margin_box.instance_variable_get(:@height)
      @margin_box.instance_variable_set(:@height, current_height + reserved)
    end

    block_height = measure_pending_footnotes_height(fns)
    available = y - margin_box.absolute_bottom
    if available < block_height
      @pending_page_footnotes = fns
      @flushing_page_footnotes = false
      return
    end

    saved_bounds = @bounding_box
    saved_y = y
    body_width = full_body_width
    begin
      canvas do
        bounding_box([page.margins[:left], margin_box.absolute_bottom + block_height], width: body_width, height: block_height) do
          move_down FOOTNOTE_RULE_TOP_PADDING
          stroke_color FOOTNOTE_RULE_COLOR
          line_width 0.5
          stroke_horizontal_line 0, body_width * FOOTNOTE_RULE_WIDTH_RATIO
          move_down FOOTNOTE_RULE_BOTTOM_PADDING

          theme_font :footnotes do
            item_spacing = (@theme.footnotes_item_spacing || 3).to_f
            index_offset = @rendered_footnotes.length
            fns.each_with_index do |fn, i|
              index = fn.index
              label = index - index_offset
              ink_prose %(<a id="_footnotedef_#{index}">#{Asciidoctor::PDF::Converter::DummyText}</a>[<a anchor="_footnoteref_#{index}">#{label}</a>] #{fn.text}),
                        margin_bottom: (i < fns.length - 1 ? item_spacing : 0),
                        hyphenate: true
            end
            @rendered_footnotes += fns
          end
        end
      end
    ensure
      @bounding_box = saved_bounds
      self.y = saved_y
      @flushing_page_footnotes = false
    end
  end
end

Asciidoctor::PDF::Converter.prepend SetadesPageFootnotes
