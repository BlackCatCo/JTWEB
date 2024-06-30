# JTWEB
The world wide web reimagined. 

TODO: more description 

## Contents:
- [JWEB Definitions](#jweb-markdown-proposed-definitions)
- [TWEB Protocol](#tweb-protocol-definitions)
- - [Client to Server](#client-to-server)
- - [Server to Client](#server-to-client)
- - [Cupcakes](#cupcakes)


## JWEB Markdown (proposed and limited) Definitions: 
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

The TWEB Protocol sends packets using [INET](https://stackoverflow.com/questions/1593946/what-is-af-inet-and-why-do-i-need-it) (IPv4). It is probably going to use port 4242 or some other four-digit number. Packets are arrays of bytes sent over the internet in this case (a.k.a. buffers). Python's fancy datatypes like strings, dictionaries, lists etc must be encoded to and properly decoded from bytes.

For example, if one would like to send a string, I would have to specify the size of this string because the receiver would not know. I could also supply an end character (0x00 or '\0'; in other words, just a byte equal to zero) so that the reciever could iterate over the string till it finds the end character, but for this case I do not see a purpose for that because I will already be supplying the size.

Think of an example string buffer like this:

`[ 05, 00, 'H', 'e', 'l', 'l', 'o' ]`

Ignoring those numbers at the beginning, note that every argument is a number. In C and in the case of packets, single character declarations are actually numbers (yes, '0' + '0' = '`' = 0x60 = 96; this is because the [ASCII code](https://images.saymedia-content.com/.image/t_share/MTc2MjU5OTkxNjc3MjQ4Njg1/what-are-ascii-codes.gif) for '0' = 0x30 = 48).

Also note that numbers of the format "\x00" (Python example) or 0x00 (C example) are in hexadecimal or base 16. Thus 0x10 = 16. (Colors are also hexadecimal values: #C0FFEE = 0xC0FFEE = 12,648,430.)

~~Now, what are those numbers? Both of those are the length of the string... just in reversed order. Following [big endian](https://en.wikipedia.org/wiki/Endianness) logic, those bytes would appear like: `[ 00, 05, ... ]` so that if the [least significant byte](https://en.wikipedia.org/wiki/Bit_numbering) were to overflow (become greater than 0xFF = 255) then the most significant byte would increment. Herein lies the confusion: most computers are little endian, thus when the LsB overflows, the next byte (the one to the right / with +1 index value) increments~~ (for networking in general big endian numbers are used). ~~Thus, the LsB comes before the MsB.~~ (This project now uses big endian numbers for networking.) The reason I'm choosing to store a generic string length using 2 bytes instead of 1 byte is that 2 bytes can store unsigned integers (whole numbers) up to 65,535 instead of a single byte's miniscule 255.

### Client to Server:
#### Instructions
| Opcode | Definition |
| - | - |
| 0x01 | [DNS Request](#dns-request) |
| 0x02 | [FETCH Request](#fetch-request) |
| 0x03 | [PUT Request](#put-request) |

#### DNS Request
A string with a single length byte out in front, for example:

`[0A, 'T', 'h', 'b', 'o', 'p', '.', 'c', 'o', 'd', 'e']`

A single byte for domain length is reasonable because it is simpler to not use domains with a string length longer than 255 characters.

Thus, the entire packet would be:

`[01, 0A, 'T', 'h', 'b', 'o', 'p', '.', 'c', 'o', 'd', 'e']`

The DNS server only accepts the domain and returns an ip address. The resource path (thbop.code/this/stuff/here).

#### FETCH Request
The FETCH request communicates with the website server and provides a resource path defining the requested resource (e.g. website page). It also provides [cupcakes](#cupcakes) in a comma-separated dictionary.

For simplicity, I am going to abstract strings to a more familiar form:

`str[u16] = "Hello world!"`

This is just custom notation to describe a string with an unsigned 16 bit integer (unsigned short) describing the string's length. In packet form, this string would be:

`[00, 0C, 'H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!']`

Thus, the FETCH request can be defined as:

```
02                                            // OPCODE
str[u16] = "resource/path/here"               // Resource path; '/' = 0x2F
str[u16] = "key1=4353,key2=654234"            // Cupcakes; '=' = 0x3D and ',' = 0x2C
```

#### PUT Request

The PUT request is similar to the [FETCH](#fetch-request) except that it sends arbitrary user input data (e.g. form data) to the server in a comma-separated list. The PUT request is defined as:

```
03                                            // OPCODE
str[u16] = "resource/path/here"               // Resource path; '/' = 0x2F
str[u16] = "key1=4353,key2=654234"            // Input data; '=' = 0x3D and ',' = 0x2C
str[u16] = "key1=4353,key2=654234"            // Cupcakes
```

### Server to Client
#### Instructions
| Opcode | Definition |
| - | - |
| 0x01 | [DNS Response](#dns-response) |
| 0x02 | [FETCH Response](#fetch-response) |
| 0x03 | [PUT Response](#put-response) |

Server responses will usually follow the format of:

```
OPCODE
ERROR CODE // one byte
DATA
```

Here's a list of error codes:
| Code | Error |
| - | - |
| 0x00 | Opcode invalid or not found |
| 0x01 | DNS resource not found |
| 0x02 | Success |
| 0x03 | Empty route |
| 0x04 | Route not found; the "404" response |
| 0x05 | Response is too big, exceeding ~67 megabytes |

#### DNS Response

Here's an example of a DNS response:
```
01                                            // OPCODE
u8                                            // Error code. "u8" means an unsigned byte
u32                                           // IP address described as four bytes
u16                                           // Port
```

#### FETCH Response

Here's an example of a FETCH response:
```
02                                            // OPCODE
u8                                            // Error code
u16                                           // Amount of chunks
u16                                           // Current chunk id; max is chunk_count-1
str[u16] = "..."                              // Content
str[u16] = "key1=packet_loss_pigeon"          // Cupcake setter
```

The server will send response packets in chunks of 1024 bytes (2^10), thus content and Cupcake setters (only appearing on the last chunk) must not, when combined, exceed 1020 bytes (again, if the current chunk is not the current chunk, only the content string is present).

#### PUT Response

Exactly the same to the FETCH response except it has a an opcode of 0x03.

### Cupcakes

They're just cookies. For example, to model a simple transaction of a user logging in and staying logged in, User A sends a [PUT request](#put-request) to a server containing login information. The server processes this and returns with a [PUT response](#put-response) containing a cupcake with User A's authorization token. This cupcake containing the token is saved to the user's browser categorized by domain/ip address (of websites). Thus, the user stores and sends different cupcakes per website. Furthermore, whenever User A does any action on the website he logged-in to, the cupcake containing his token will also be sent with all his traffic and will properly authorize that all his actions belong to his particular account.