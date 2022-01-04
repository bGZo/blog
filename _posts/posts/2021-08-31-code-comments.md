---
layout: post
title: Code Comments
updated: 2021-08-31
category: posts
---


> “Programs must be written for people to read and only incidentally for machines to execute.” -- MIT professor Hal Abelson

![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/comments_post.webp)

Once I wrote my blog to comments (knowledge, archive progress and feeling). That's almost a disaster. All code is in a mess without identity. Continuously changing the same code over and over again. Even though it looks pretty funny and full-details. But it seems just stop to the surface you first look. I found a [article](https://stackoverflow.blog/2021/07/05/best-practices-for-writing-code-comments/) from StackoverFlow saying comments. I take it contents and examples, like following:

- **Comments should not duplicate the code.**

  ```cpp
  // create a for loop // <-- comment
  for // start for loop
  (   // round bracket
      // newline
  int // type for declaration
  i    // name for declaration
  =   // assignment operator for declaration
  0   // start value for i
  ```

- **Good comments do not excuse unclear code.**

  ```java
  private static Node getBestChildNode(Node node) {
      Node bestNode; //bestNode raw: n 
      for (Node currentNode: node.getChildren()) {//currentNode raw: node
          if (bestNode == null || utility(currentNode) > utility(bestNode)) {
              bestNode = currentNode;
          }
      }
      return bestNode;
  } 
  ```

- **If you can’t write a clear comment, there may be a problem with the code.**

  > Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it. -- [Kernighan’s Law](https://github.com/dwmkerr/hacker-laws#kernighans-law)

- **Comments should dispel confusion, not cause it.**

- **Explain unidiomatic code in comments.**
  Otherwise someone might “simplify” the code or view it as a mysterious but essential incantation. And don't bring other language omit to another, which [somtime](https://kotlinlang.org/docs/idioms.html#nullable-boolean) make no sence.

- **Provide links to the original source of copied code.**
   Of course, you should [never paste in code that you don’t understand](https://stackoverflow.blog/2019/11/26/copying-code-from-stack-overflow-you-might-be-spreading-security-vulnerabilities/).

  ```cpp
  /** Converts a Drawable to Bitmap. via https://stackoverflow.com/a/46018816/2219998. */
  // Many thanks to Chris Veness at http://www.movable-type.co.uk/scripts/latlong.html
  // for a great reference and examples.
  ```

- **Include links to external references where they will be most helpful.**

  ```cpp
  // http://tools.ietf.org/html/rfc4180 suggests that CSV lines
  // should be terminated by CRLF, hence the \r\n.
  csvStringBuilder.append("\r\n");
  ```

- **Add comments when fixing bugs.**

  ```cpp
    // NOTE: At least in Firefox 2, if the user drags outside of the browser window,
    // mouse-move (and even mouse-down) events will not be received until
    // the user drags back inside the window. A workaround for this issue
    // exists in the implementation for onMouseLeave().
    @Override
    public void onMouseMove(Widget sender, int x, int y) { .. }
  
  // Use the name as the title if the properties did not include one (issue #1425)
  ```

- **Use comments to mark incomplete implementations.**

  ```cpp
  // TODO(hal): We are making the decimal separator be a period, 
  // regardless of the locale of the phone. We need to think about 
  // how to allow comma as decimal separator, which will require 
  // updating number parsing and other places that transform numbers 
  // to strings, such as FormatAsDecimal
  ```

  - `NOTE`: Description of how the code works (when it isn't self evident).
  - `XXX`: Warning about possible pitfalls, can be used as `NOTE:XXX:`.
  - `HACK`: Not very well written or malformed code to circumvent a problem/bug. Should be used as `HACK:FIXME:`.
  - `FIXME`: This works, sort of, but it could be done better. (usually code written in a hurry that needs rewriting).
  - `BUG`: There is a problem here.
  - `TODO`: No problem, but additional code needs to be written, usually when you are skipping something.
