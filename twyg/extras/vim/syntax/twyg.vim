" Vim syntax file
" Language:   twyg configuration
" Maintainer: John Novak <john@johnnovak.net>

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syntax case match

"------------------------------------------------------------------------------
" GENERAL
"------------------------------------------------------------------------------
" Configuration sections
syn match   twygSection     "\[layout\]\|\[node\]\|\[connection\]\|\[color\]"

" Levels
syn match   twygLevel       "{.*}"

" Directives
syn match   twygDirective   "@copy\|@include"

" Functions
syn keyword twygFunction    abs ceil floor log log10 max min pow round sqrt
syn keyword twygFunction    rgb rgba hsl hsla darken lighten blend

" Variables 
syn keyword twygVariable    x y width height bboxWidth bboxHeight
syn keyword twygVariable    textWidth textHeight maxTextWidth lineHeight 
syn keyword twygVariable    fontSize fontColor bgColor baseColor
syn keyword twygVariable    color fillColor strokeColor

" Styles
syn keyword twygNodeStyle       box oval poly rect
syn keyword twygConnectionStyle curve junction
syn keyword twygLayoutStyle     layout
syn keyword twygColorStyle      colorizer

" Comments
syn match   twygComment     "--.*$" contains=twygTodo

" Todo
syn keyword twygTodo        contained TODO FIXME XXX DEBUG NOTE

"------------------------------------------------------------------------------
" CONSTANTS
"------------------------------------------------------------------------------
" Numbers
syn match   twygNumber      "-\=\<\d*\.\=[0-9_]\>"

" Strings
syn match   twygString      +"[^"]*"+

" Booleans
syn keyword twygBoolean     yes no true false

" Colors
syn match   twygColor       "#[0-9A-Fa-f]\{3\}\>"
syn match   twygColor       "#[0-9A-Fa-f]\{6\}\>"

"------------------------------------------------------------------------------
" ENUMS
"------------------------------------------------------------------------------
" Enum values
syn keyword twygLevelOrientationValue   top right bottom left any
syn keyword tywgCornerStyleValue        square beveled rounded
syn keyword twygJunctionStyleValue      none square disc diamond
syn keyword twygJunctionSignValue       none plus minus
syn keyword twygBoxOrientationValue     topleft topright bottomleft bottomright
syn keyword twygTextAlignValue          left right center justify auto
syn keyword twygRoundingStyleValue      screen arc

"------------------------------------------------------------------------------
" PROPERTIES
"------------------------------------------------------------------------------
" Style properties
syn keyword twygStyleProperty   style

" Level selector properties
syn keyword twygLevelSelector   levelDepthMin levelDepthMax 
syn keyword twygLevelSelector   levelNumChildrenMin levelNumChildrenMax
syn keyword twygLevelSelector   levelOrientation

" Layout properties
syn keyword twygLayoutProperty  horizontalBalance verticalAlignFactor
syn keyword twygLayoutProperty  rootPadX nodePadX nodePadY sameWidthSiblings
syn keyword twygLayoutProperty  snapParentToChildren snapToHalfPositions
syn keyword twygLayoutProperty  branchPadY radialMinNodes radialFactor

" Common node properties
syn keyword twygNodeProperty  fontName fontSize lineHeight textAlign 
syn keyword twygNodeProperty  justifyMinLines hyphenate maxTextWidth
syn keyword twygNodeProperty  textPadX textPadY textBaselineCorrection
syn keyword twygNodeProperty  strokeWidth 
syn keyword twygNodeProperty  nodeDrawShadow nodeShadowColor
syn keyword twygNodeProperty  nodeShadowBlur nodeShadowOffsX nodeShadowOffsY
syn keyword twygNodeProperty  textDrawShadow textShadowColor 
syn keyword twygNodeProperty  textShadowOffsX textShadowOffsY 
syn keyword twygNodeProperty  drawGradient gradientTopColor gradientBottomColor

" 'box' node style properties
syn keyword twygNodeProperty  boxOrientation boxDepth horizSideColor
syn keyword twygNodeProperty  vertSideColor strokeColor

" 'oval' node style properties
syn keyword twygNodeProperty  aspectRatio maxWidth

" 'poly' node style properties
syn keyword twygNodeProperty  numSides rotation

" 'rect' node style properties
syn keyword twygNodeProperty  roundness cornerRadius roundingStyle

" 'curve' connection style properties
syn keyword twygConnectionProperty  nodeLineWidthStart nodeLineWidthEnd
syn keyword twygConnectionProperty  nodeCx1Factor nodeCx2Factor
syn keyword twygConnectionProperty  nodeCy1Factor nodeCy2Factor

" 'junction' connection style properties
syn keyword twygConnectionProperty  lineWidth junctionXFactor
syn keyword twygConnectionProperty  cornerStyle cornerRadius
syn keyword twygConnectionProperty  junctionStyle junctionRadius
syn keyword twygConnectionProperty  junctionFillColor 
syn keyword twygConnectionProperty  junctionStrokeWidth junctionStrokeColor
syn keyword twygConnectionProperty  junctionSign junctionSignSize
syn keyword twygConnectionProperty  junctionSignStrokeWidth junctionSignColor

" Color properties
syn keyword twygColorProperty  colorscheme
syn keyword twygColorProperty  fillColor strokeColor connectionColor fontColor
syn keyword twygColorProperty  fontColorAuto fontColorAutoDark
syn keyword twygColorProperty  fontColorAutoLight fontColorAutoThreshold
syn keyword twygColorProperty  backgroundColor rootColor nodeColors


" Define the default highlighting.
" " For version 5.7 and earlier: only when not done already
" " For version 5.8 and later: only when an item doesn't have highlighting yet
if version >= 508 || !exists("did_css_syntax_inits")
  if version < 508
    let did_css_syntax_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif

  HiLink twygSection                Type
  HiLink twygLevel                  Special
  HiLink twygDirective              PreProc
  HiLink twygFunction               Statement
  HiLink twygVariable               Identifier

  HiLink twygStyleProperty          Identifier
  HiLink twygLayoutProperty         Identifier
  HiLink twygNodeProperty           Identifier
  HiLink twygConnectionProperty     Identifier
  HiLink twygColorProperty          Identifier
  HiLink twygLevelSelector          Special

  HiLink twygNumber                 Number
  HiLink twygString                 String
  HiLink twygBoolean                Constant
  HiLink twygColor                  Special

  HiLink twygLevelOrientationValue  Constant
  HiLink tywgCornerStyleValue       Constant
  HiLink twygJunctionStyleValue     Constant
  HiLink twygJunctionSignValue      Constant
  HiLink twygBoxOrientationValue    Constant
  HiLink twygTextAlignValue         Constant
  HiLink twygRoundingStyleValue     Constant

  HiLink twygNodeStyle              Constant
  HiLink twygConnectionStyle        Constant
  HiLink twygLayoutStyle            Constant
  HiLink twygColorStyle             Constant

  HiLink twygComment                Comment
  HiLink twygTodo                   Todo

  delcommand HiLink
endif

let b:current_syntax = "twyg"

