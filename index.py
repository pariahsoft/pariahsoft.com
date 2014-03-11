###################################
## PariahSoft.com Website        ##
## index.py                      ##
## Copyright 2014 PariahSoft LLC ##
###################################

## **********
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to
## deal in the Software without restriction, including without limitation the
## rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
## sell copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
## IN THE SOFTWARE.
## **********

import cgi
import json


class PageBuilder:
    def __init__(self, config, name, page):
        self.config = config
        self.name = name
        self.page = page

        self.formatdict = dict(list(self.config.items()) + list(self.page.items()))

        self.httpheader = "Content-type: text/html; charset=utf-8\n\n"
        self.html = ""

    def build(self):
        # Call the page section builders in order.
        self.__build_header()
        self.__build_content()
        self.__build_footer()

        # Return the page content.
        if not __name__ == "__main__":
            return self.httpheader + self.html
        else:
            return self.html

    def read(self, filename):
        with open(filename, "r") as f:
            content = f.read()

        return content

    ########################################
    # Page section builders go under here. #
    ########################################

    def __build_header(self):
        content = self.read(self.config["header"])
        content = content.format(**self.formatdict)

        self.html += content

    def __build_content(self):
        content = self.read(self.page["content"])
        content = content.format(**self.formatdict)

        self.html += content

    def __build_footer(self):
        content = self.read(self.config["footer"])
        content = content.format(**self.formatdict)

        self.html += content


def main():
    """Build and deliver the webpage.

    This function reads the configuration files and client request, selects the page to be delivered, and instructs
    PageBuilder to build and return the page content. The content is then delivered through the resident HTTP server.
    """
    # Read the config file.
    with open("config/config.json", "r") as f:
        config = json.load(f)

    # Read the pages file.
    with open("config/pages.json", "r") as f:
        pages = json.load(f)

    # Receive HTTP request fields.
    fields = cgi.FieldStorage()

    # Did the client request a page?
    if "page" in fields:
        pagename = fields["page"].value.lower()

        # A known page was requested. Select this one from the pages file.
        if pagename in pages:
            target = (pagename, pages[pagename])

        # Unknown page name. Select the 404 page.
        else:
            target = ("404", pages["404"])

    # No page requested. Select the default page.
    else:
        target = ("default", pages["default"])

    # Initialize PageBuilder, build the page, and deliver the resulting HTTP header and HTML.
    print(PageBuilder(config, *target).build())

# Run the script.
main()
