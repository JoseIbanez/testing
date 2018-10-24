

tagTpl = """
<svg xmlns="http://www.w3.org/2000/svg" width="90" height="20">

  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>

  <rect rx="3" width="90" height="20" fill="#555"/>
  <rect rx="3" x="37" width="53" height="20" fill="#4c1"/>
  <path fill="#4c1" d="M37 0h4v20h-4z"/>
  <rect rx="3" width="90" height="20" fill="url(#a)"/>

  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="19.5" y="15" fill="#010101" fill-opacity=".3">{{text1}}</text>
    <text x="19.5" y="14">{{text1}}</text>
    <text x="62.5" y="15" fill="#010101" fill-opacity=".3">{{text2}}</text>
    <text x="62.5" y="14">{{text2}}</text>
  </g>

</svg>
"""

class Tag:

    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2


    def getSVG(self):
        out = tagTpl.replace("{{text1}}", self.text1).replace("{{text2}}", self.text2)
        return out

