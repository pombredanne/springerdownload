
from util import decodeForSure
from time import localtime, strftime
   
################################################################################
############################# meta to pdfmark  #################################
################################################################################

def _uniconvHex(s):
   out = ""; s = decodeForSure(s)
   for c in s:
      out += str(hex(ord(c)))[2:].upper().rjust(4,"0")
   return out

def infoToPdfmark(i):
   marks = "["
   for x,v in zip(['title','subtitle','authors','year'],\
                  ['/Title','/Subject','/Author','/CreationDate']):
      if i[x]: 
         s = ", ".join(i[x]) if x == 'authors' else i[x]
         if x == 'year': s = "(D:%s)" % (s)
         else: s = "<FEFF"+_uniconvHex(s)+">"
         marks += " %s %s" % (v,s)
   marks += " /ModDate (D:%s)" % (strftime("%Y%m%d%H%M%S",localtime())) \
         +  " /Creator (springer_download.py)" \
         +  " /Producer (springer_download.py)" \
         +  " /DOCINFO pdfmark\n"
   return marks

def tocToPdfmark(toc,filt=lambda x:x):
   marks = ""
   for a,b,c,d in toc:
      marks += "["
      if d > 0: marks += "/Count -%d " % (d)
      marks += "/Title <FEFF%s> /View [/XYZ null null null] /Page %d  /OUT pdfmark\n" \
                           % (_uniconvHex(filt(a.strip())),b)
   return marks
   
def labelsToPdfmark(pls):
   if len(pls) == 0: return ""
   mark = "[/_objdef {pl} /type /dict /OBJ pdfmark\n[{pl} <</Nums ["
   tmp = []
   for label in pls:
      tmp2 = ["%s %s" % (i,j) for (i,j) in label[1].items()]
      tmp.append("%d <<%s>>" % (label[0]," ".join(tmp2)))
   mark += " ".join(tmp)
   mark += "]>> /PUT pdfmark\n"
   mark += "[{Catalog} <</PageLabels {pl}>> /PUT pdfmark"
   return mark
   
