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

// TODO: add a button/link and text input

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

## TWEB Protocol Definitions:

The TWEB Protocol sends packets using [INET](https://stackoverflow.com/questions/1593946/what-is-af-inet-and-why-do-i-need-it) (IPv4). Packets are arrays of bytes sent over the internet in this case (a.k.a. buffers). Python's fancy datatypes like strings, dictionaries, lists etc must be encoded to and properly decoded from bytes.

For example, if one would like to send a string, I would have to specify the size of this string because the receiver would not know. I could also supply an end character (0x00 or '\0'; in other words, just a byte equal to zero) but for this case I do not see a purpose for that because I will already be supplying the size.

Think of an example buffer like this:

`[ 05, 00, 'H', 'e', 'l', 'l', 'o' ]`

Ignoring those numbers at the beginning, note that every argument is a number. In C and in the case of packets, single character declarations are actually numbers (yes, '0' + '0' = 0x60 = 96; this is because the [ASCII code](https://images.saymedia-content.com/.image/t_share/MTc2MjU5OTkxNjc3MjQ4Njg1/what-are-ascii-codes.gif) for '0' = 0x30 = 48).

Also note that numbers of the format "\x00" (Python example) or 0x00 (C example) are in hexadecimal or base 16. Thus 0x10 = 16. (Colors are also hexadecimal values: #C0FFEE = 0xC0FFEE = 12,648,430.)

Now, what are those numbers? Both of those are the length of the string... just in reversed order. Following [Big Endian](https://en.wikipedia.org/wiki/Endianness) logic, those bytes would appear like: `[ 00, 05, ... ]` so that if the [least significant byte](https://en.wikipedia.org/wiki/Bit_numbering) were to overflow (become greater than 0xFF = 255) then the most significant byte would increment. Herein lies the confusion: most computers are little endian, thus when the LsB overflows, the next byte (the one to the right / with +1 index value) increments. Thus, the LsB comes before the MsB. The reason I'm choosing to store a generic string length using 2 bytes instead of 1 byte is that 2 bytes can store unsigned integers (whole numbers) up to 65,535 instead of a single byte's miniscule 255.

### Client to Server:
#### Instructions
| Opcode | Definition |
| - | - |
| 0x01 | [DNS Request](#dns-request) |
| 0x02 | [Fetch Request](#fetch-request) |
| 0x03 | [Put Request](#put-request) |

#### DNS Request

#### Fetch Request

#### Put Request
