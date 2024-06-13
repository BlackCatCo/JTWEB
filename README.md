# JTWEB
The world wide web reimagined. 

TODO: more description 

## Contents:
- [JWEB Definitions](#jweb-markdown-proposed-definitions)
- [TWEB Protocol](#tweb-protocol-definitions)


## JWEB Markdown (proposed) Definitions: 
```
// This is a comment... similar but unlike CSS comments
def DOCUMENT { // All caps definitions are system overrides
    bg-color: #000000;
    txt-color: #eaeaea;
}

def colortxt(color c, str v) { // Color and value string passed as arguments
    txt-color: c;
    value: v;
}
def redtxt(str v) { // Color literal and string value passed into parent
    from: colortxt( #ff0000, v );
}



"Hello World!";

redtxt("This text is always red!");

colortxt(#00ff00, "This text is green!");

```

HTML Equivalent:
```html
<html>
    <head>
        <style>
            * {
                background: #000;
                color: #eaeaea;
            }
            .red {
                color: #f33;
            }
            .green {
                color: #0f0;
            }

        </style>
    </head>
    <body>
        <p>Hello World!</p>
        <p class="red">This text is always red!</p>
        <p class="green">This text is green!</p>
    </body>
</html>

```


The system will handle rendering directly, not translating to html for Chromium or Gecko to render.

### Variable Types:

| Name      | Description     |
| - | - |
| def | The definition type; defined with "def" and parentheses (possibly with arguments). |
| str       | The string type; literals are enclosed in double quotes: "" |
| color     | An 18 bit integer describing 3 channels (red, green, and blue) each as 1 byte. Literals begin with hashtag: #  |

### System Overrides:
| Name | Description |
| - | - |
| DOCUMENT | Overrides properties for the entire document. |

### Properties:
| Name | Description |
| - | - |
| bg-color | Defines the background color in that definition; accepts a color. |
| txt-color | Defines the text color in that definition; accepts a color. |
| value | Defines the displayed text for that definition; accepts a string. |
| from | Definition inheritence; default: DOCUMENT (no arguments). Accepts a definition-- most likely one with arguments (thus the parentheses). |

## TWEB Protocol Definitions
TODO: this...