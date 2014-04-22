import sys
import png


def chunck(a, s):
  for i in xrange(0, len(a), s):
    yield a[i:i+s]

with open(sys.argv[1], 'r') as f:
  i = 3
  pixels = []
  linePixel = []
  lc = 30
  rest = []
  for l in f:
    if i>0:
      i-=1
    else:
      a = rest + l.split(' ')[:-1]
      for ind,tr in enumerate(a):
        a[ind] = int(tr)
      s = len(a)/3 * 3
      rest = a[s:]
      a = a[:s]
      for ch in chunck(a,3):
        if ch[0] == -1:
          ch = 4*[0]
        else:
          ch.append(255)
        linePixel += 2*ch
        lc -= 1
        if lc == 0:
          lc = 30
          pixels.append(linePixel)
          pixels.append(linePixel)
          linePixel = []

image = png.from_array(pixels, 'RGBA')
image.save(sys.argv[1][:-5]+'.png')
