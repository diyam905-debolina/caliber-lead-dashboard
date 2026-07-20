import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io, base64

st.set_page_config(page_title="Caliber Lead Analytics", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

CALIBER_LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCABkAPYDASIAAhEBAxEB/8QAHQABAAIDAQEBAQAAAAAAAAAAAAcIBAUGAwIBCf/EAEMQAAEDAwEFBQQECwgDAAAAAAECAwQABREGBxITITFBUWFxgQgUIjIVYpGhIzNCUnJ1krGzwcIXJCU2N4Ky0kOV8P/EABwBAQACAwEBAQAAAAAAAAAAAAADBgEEBQIHCP/EADYRAAEDAwIDBQcDAwUAAAAAAAEAAgMEBREhMRJBUQYTImFxI4GRocHR4RQysQcVUjVCovDx/9oADAMBAAIRAxEAPwC5dKUoiUpXjNlRoUVyVMkNR2GxvLcdWEpSO8k0WCQBkr2rWajv9o09BM28TmorX5O8fiWe5KRzUfKos15tsjscSFpNkSHOYM15JCE/oJ6q8zgeBqFLzdbleZy510mvS5C+q3VZwO4dgHgOVbDICdSqfde19PTZjpvG7r/tH393xUma82z3O5cSFpptdtinl7wrBfWPDsR6ZPiK7X2a3nn9Dz3H3VurN1cJUtRJOW2ieZ8TVcasX7Mn+Qp360c/hNVJKwNZouH2cuNTXXYPndnQ+g9ApTpSlaa+mpSlKIlKUoiUpSiJSlKIlKUoiUpSiJSlKIlKUoiUpSiJSlKIlKUoiUPIZNcprjX+ndJNqROk8ebjKIbBCnD3Z7EjxPpmoD13tM1FqkuR+L9H25XL3VhRG8Prq6q8uQ8KlZC564F17R0luy0nif0H1PL+fJTBrza5YbBxIlrKbtcE5BDSvwLZ+svt8k57iRUDav1ff9VSuNd5ynGwctx0fC035J/mcnxrQ0rcZE1my+a3S/1dxOHnDf8AEbe/r70pSlSLipVi/Zk/yFO/Wjn8Jqq6VYv2ZP8AIU79aOfwmqgqP2K09jv9SHoVKdKVAO3HaPImTpGmbHIU1DZUW5b7ZwXljkUA/mjoe8+HXUYwvOAvo91ukNsg72TXoOZP/dypJ1NtR0dYnlx3bgqbIQcKaho4hB7t7ITnwzXPNbddLqd3XLZd0Iz8242ftG/UYaC2Yag1WwmcNy325XyyHwSXP0EjmfPkPGu6f2Bs+7YY1K5xwOq4g3T6BWR99TlkTdCVVY7l2hrW99BEA3ltr8Tk+qkvSms9OaoSRaLk268BlTCwUOp/2nmR4jI8a6CqwwNmetIeto9qZQqM6gh1NxZUeEhAPzhXI5+ryPpzqzMNtxmIyy8+qQ4htKVuqABcIGCogcgT15VFIxrf2lWCx3GrrGOFVFwOacZ5H3HX6L1pXjNlxYUdUiZJZjMp+Zx1YQkeZPKtbbtVaauMoRIN/tkl8nCW25KCpR8Bnn6VHgrsOmjY4Nc4AnllbilY0m4QIrnDkzozK8Z3XHUpOO/BNfapUcQ1TEuocYSgr30KBBA64PSsL3xt1GdlHEjbLYm785aEWu5OuplGMFp3N1SgrdyPi6E10W0jXFv0Tb478qO7KflLKWGEEJ3t3G8ST0AyO/qKrjs9aXdNpFm4g3lO3FDyx34Vvn9xqets2koerIEJCrxFt06IpamPeFgIWlWN4Ht/JTzGenjWy+NjXAFUu3Xa411BUTMILwQG6Aevvxtnmtps31xb9bQJD0WO7FkRlBLzDigrdCs7pBHUHB7uhrn9R7Y7FZL7MtL1tuDzsR0tLW3ubpI64yqs7Y5ohrSNslPm4sXCTOUnfdY5tpSjICUnt5k5PLuxyqAVH6b2mnnve/3n/m96d9GRsc49EuN2uNHRU/FgSvJzoD6eXMbK3SCVISopKSRkg9RX7WpuuptO2p/gXK+W6I92tuyEpWPTOazbdPg3GP7xb5saYyTjiMOpcT9oOK18FXFs0bncAcCRyzqsmlKKISCSQAOZJ7KwpUpWikax0nHf4D2pbShzOCky0cj48+XrW4iSY0yOmREkNSGV/K40sKSfIjlWSCFEyeKQkMcCR0K9aUUQkEkgAcyT2Vix7jb5Doajz4rzh6IQ8lRPoDWF7LgDglZVK1kLUFimzHYcO82+RIZGXGm5CVKSM45gHv5UrOF5bKx4y1wKg/U+lrfebjNd5xpJfc/CoHX4j8w7f3+NR3ftOXSzHeks77HY+3zR693rUwKUFXKYB2PuZ/aNZSEpWgoWkKSQQQRkEV8You29faKh0b/aRgnwnceh5emo8lLe+xNvurO9YO7k6jY+o2ProfNV+pUrak2ewpwVItK0wnzzLZ/FKP70+nLwqNrxabjaJPAuEVxhR+UkZSryI5Hr2V9YsXaq3XtuKd+H82nR3w5jzGV8ZvPZuvtDvbty3k4aj8ehwsKlbTTWnrzqOcIdmgOynOW+UjCEDvUo8gPOp00HsZtVr4czUa0XSWMEMAHgIPiDzX64HhXffI1m6gtlkq7ifZNw3qdvz7lEGiNBai1a4FQIvBh5wuW/lLQ78dqj4DPjirJ7PdKRdHadTaYz65ClOl551QxvrIAJA7BhIGPCugaQhptLbaEoQkYSlIwAO4CvqtOSUv05L6ZZuztPbPGDxP6n6D/0rn9o93csOh7tdGVFLzTBS0ofkrUQhJ9CoGq2bKdON6p1vEt8oFUVGX5PPmpCez1JA9an3bnHckbLrulveKkBpwgdoS6knPpk+lRD7OM1iJtDUy8oJVLhOMNZ7VbyF4+xBqWLSMkLhdoQJ71TQy/s0+ZP84AVkmm22mkNNIS22hISlKRgJA6ADsFfVKVqq+7JWq1dfYmmtPS7zNyW46MhAOC4o8kpHmSPLrW1qGvajmuN2myW9JIbffdeUO8oSkD+Ia9xt4nALm3itNDRSTt3A09ScD5lRbd7rqjaFqNKFB+dJdUeBFZ/FtD6o6ADtUfU1trnsk1tbrcZ/uTL+4N5TUd4KdSB247f9uTUh+zJaY7WnbheihJlPyTHCu1LaEpOB3ZKjnyFS9U75iw8LRsqha+zEdwphVVb3F79d9unqqY3y8XG9Psv3OQqQ+ywlgOL+YpTnGT2nn1/nVlE5smwvtQ41Ys+Timv+yqr/tBiMf2j3iFb0pCFXBaEJHQKKuY9FEip923uot2yifGa+EKDMdvy30/0g16l14QtSwNdAK2Z5yWNIz13+yh3YBE952nQXMZEZp50/sFI+9QrYe0pK4+v2WAeUeC2gjxKlq/cRWZ7MMXf1VdJpGeDC4fkVrSf6DXLba5Xve068rBylDiGh4bjaUn7wa9by+gWk/2PZ5o/zk/gfhTrs4/wXY5AkHlwbe5K+3ec/nVYbW/Mi3GO/b1OJloWOCWxlQX2bvjnpVnta/4JsWlx/l4NpRF+1CW8ffUR+zna40/Xi5UhIX7jFU80D+eVJSD6BR9cV4idgOcupfaV01TRULDgho92wz/xXnH2O64nRFT30w2nl/GWX5J4yie/AIz5mud07eb/AKB1WVBDsaRHcCJcRZwlxPalXZ06HyIq3NVy9pdEZOvIqmgA8u3oL2O076wCfHAHoBSOUvPC5YvlghtVO2rpXkOaRud/P1VgrbcYs+0R7ow4PdX2EvpWo4wkjPPu5dardtV2h3DVlzXbra46zZ0L3GmUEgyDn5lY657E9nLtrvI06VC9mIyN4h0xVMg5/IXILf8AxVUJ6ak3OBeGbhaGFPS4x4jeGOLunpvbuCOWeR7DikMYBJ6LPaS7yyxQQAlokaHOxvg8v505rqYeyXXMm3iWm1oa3hvJZdfShwjyJ5eRwa1mktR37QepDuh9ktObkyE5lIcA6gg9D3H+VdJ/aRtS7n//AFqf+tcrqd7VGpLobndbdKclKQEKWiGUbwHTIA5nsz4CpRxHR2MLgVH6SDgkoO8EgPMD6KzOprxGd2cXG9w3N9h22OPMq795s7vkckVVKxquZniLaeKZUxPuyUtfMsLwCkHsz0PgTU0SJEmD7MSUSkuNSFoLAS4ndUAZRGMH6lc37NdsRL1tIuDiN4QYiig4+VayEg/s79RR4Y1xXcvJfc66kizwlzQT5cWp+QXebDtA3HSi7hcL000ia+lLLSUOBe638yuY7zj9mlShStZzi45KvlBQxUMAgi2HxUJMqKrhMOc5kuZ/aNbFnrWohuD6RnZVhKZLvM9nxHNcbrLa3ZrOXIdkSm7zxkZQr8A2fFQ+bHLkn7RX57dZa66174KOMvdnlsPU7D3q7S1UNPCHyuwFJ0qXFgQ3Jc2SzGjtjK3XVhKUjxJ5VDu0La1Cnx3rRpy3tTkLG6qZLb/BjxQg8yR1CjjBHQ1HF9vGoNWTBIvk5b6ArebYT8LLX6Keg5csnJPaTX7GitspGBkivsPZP+klPQvbVXJ3HINQ0ZDQfXQuPwHkVRbt2k70OihGh681OuxbbNDtttjWLU1tjQWUAJROhtbqSfznEDtPaode7tqwVumw7jDbmQJTMqM6N5DrSwpKh4EVQ+ug0ZrLUOkZnvFlnraQo5cYX8TTn6SenqMHxr6bWWRknihOD05fhcaju5hAZIPCOnJXYpUW7PNtGn9Q8OFeN2zXFWAOIv8AAOH6qz08lfaalIEEAggg9CKrM9PJA7hkGCrHDPHO3ijOVj3KGxcLdJgSkb7ElpTTie9Khg/vqpOqbLdtE6rVEWtxl+M4HYshHLfSDlK0n/7BBHZVvq02rNMWXVEAQ7zDS+lOS24DuuNnvSocx2cuhxzzWIpOA67LidoLJ/c42ujOJG7H6fYqNNI7cbeuE2xqWFIalJThUiMkKQ54lOQUnwGR5Vs7rtv0rHjlUCLcJr2PhRww2nPionl6A1orpsFSXVKteoilv8luTHyR5qSRn9mvKBsEeLgM/UbaUDqlmMST6lQx9hqTEJ1XEZL2nY3uuAHz8P3x8Qt3sp2qu6k1BItN7bYjOyFb8Hh8k8hzbJPU9oPbzHcK9/aPsT9y0hHucZBcXbXitwAZIaWAFH0IT6ZPZXTaL2faa0oQ9AiF6ZjBlSCFuenLCfQDxzXUuttutLadQlxtaSlSVDIUD1BHaKjL2h/E1dyC21VRbXUtc8Fzs6jlzGeuD9lW7YttEjaREm13Zt1VukOB1LjQ3i0vABJHaCAOnMY7c13urttOn41rdTp4vTpy0ENKUyUNtkj5lb2CcdwHPvFeGp9htrmzFybJdHLalZyY7jXFQD9U5BA8DmvvTexC0QS47dbk5cXi2UtpDQQ22ojAURk72OoyQO8GpXGJx4iuFSU3aGli/RxhvCNnZGg8tc/EKG9BMuXPaBZkPKLqnrg0t0qOSob4Uon0BqaPablcPRkCIDgvzwo+SUK/mRWXo/ZDbNOakh3pu7SpK4pUpLa20hJJSU9R3Zz6VvNpOhY2tkQUSrg/ETDLhAaQFb5Vu9c92799YdI0vB5BeqGx1tPaqiEt9o86DI205/FcR7LkXdtd7m4/GPtNA/opUf66im4/47tJfSPjE+7qSO3IW9gDt7D41ZjZ9pKNo6xO2qHKdkBx9T5ccSAd4pSnoPBIrkdP7GLXab9Cu4vMyQuI+l8IW2nClJORk+dGytDnOWKqwVclFS0zW/tJLtRpk/PcrN9oiX7vs1fZ3se9SmmvPB3/AOioK2b6re0fqZu6ttcdlSCzIazgrbJBOD3ggEeVWT2i6PY1nao9ukznojbL/Gy2kEqO6Ujr+ka5uBsb04zp+VapMiRJW86HWpWAlxlQGOWOo7weR8wDSORjWYKmvNnuNVchU0+AGgYORuMnb1Povydts0gzbuPFROkySnKY/B3CD2BSjyHmM1CMp29bQtclYQHJ1wdCUoTncaQB9yUpHM+BPWpLTsD/AL0d7U/93zyxD+PHd8+PX7qkrQ+iLDpCOpNsjqXIcGHZTxCnVjuz2DwGKyHxxjw7qCS2Xi7yNZX4ZG05OMa/AnX10Cx9UaVS/suk6VgAqLUJLbGcArW3hSc+JUkfbVd9m2qn9E6q9/cjLdaUkx5THyq3cgnGfygQOviOWatrXAa92VWDVMtdwbccttwXzcdZSFIcPepB6nxBGe3NeIpAAQ7YrpX2yzzPiqaI4fHoB5DbHLTz3WJL21aNag8dgz5DxHJgMbqs9xJOPsJrB0Ltmi3u8Itd0tLsR2Q7uRlxyXQcnklQxnPiMjwFaZrYG5x/wup08IHqmF8RH7fL76kPQmz3T2kTx4TTkicU4MqQQVgHqE4GEjy595NZd3QGmqipD2hnqGmbhYwb7HPwJPzC5r2mJfB0PDig4VInpyO9KULJ+/drVey3F3YF9mlP4x1loHH5oUT/AMh91d1tI0PG1szCZk3F+IiIpagGkBW+VADnnux99ZOzvSEXRlmetsWU7KD0gvqccSAclKU45dnw/ea88Y7vh5rYNsqX3wVjh7MDAOR0xtvuSulpSlQq0KrW3XZxtHakS5MCR9I6ddcU6tqCgpcSCd48VGSVAZ6gkcskCobg21DIBUkA93bX9Ca4LaHsq01q4OSuD9G3RQyJcdI+I/XT0X58j411rPV01C3uu7DR1A59T19VyrlRz1J42vyeh+iqGkBIAAwBX7XYa+2c6l0a6pdwiceBvYRNYBU0e7e7UnwPpmuPq4RyslbxMOQqpJG+N3C8YKUpSpF4SrR+y9OlzNnDyJUhx5Ma4uMs76s7iOG2rdHhlSvtqrlWb9lL/Tuf+tnP4LNce+AfpfeF1bMT+p9xUqXO4QLXDVMuc6NCjIICnpDqW0Ak4GVKIHM1+Wu5W66xRLtc+LOjlRSHYzyXEZHUZSSM1pNoz7MWzQpUhxLbLN1huOLV0SkPoJJ8BXIXqe9KuF7v+iGnQwqLHYmTGGFAPL46d5aBukuLQyXMqAPUdSMVTVblJdwnwreyHp0pqO2okBTit0EhJUfuSo+QNesV9mVGakx3EusuoC21pOQpJGQR4EVD5kTVRSqJdZFwhsz0rjucZ58NO+6yd8JecG8r8g4yQknGeeB0Fsc1Ku92yyqemKgzUMXRcwrOW20ISHY+c5+J0NnH5rix2URSJXw+60wyt55xDTSElS1rUAlIHUknoKhqNddR+7OPvXeYm9mFLVcIgcePCKWFkfgykIaCVhG6tPzch8WcjstTW3h7MfohcmZMXcFRorrkh5Tjiy+82hZyTyGFqOBgAdAAKIuzcdaaU2lx1CC4rcbClAFSsE4HecAnHga+6iV5WoZM21quYkob0rcYsVxwjlOdddS1xvEBhxKj3F1X5tfa7ldQ228xd7uvUKnJAuUFaVhhllKHeYTu7rYSQnccGCs45qzyIpXpUQ3L6Vt8e1R7lf7mxb3bUiSuW7NkILsxWd8cRCSRgBJS1yScq+E4xUiaUuKn7bBgz5CnLsiAw/KCmlNqO8CN4gj4SSlWU9RRF7RtRaflXRdqjX21v3BClIXFbltqeSpPzAoByCMHIxyraVEtxnWubo+46cZAl6iN4uBgMNtlTrD5nPKbdzj4AMhRUSPh7edesmdfFaycTIusqLPRd0txYaXHilyJvj/whHDWhTeSpwklJz8QxiiKSLfdrbcXnWYM5iS4yhK3EtrCilKioJJ8yhX2Gs2ojsku82+0yLlFVMcbs7ceUuGgnD7Jckh9ISeRVuHfH1kJ769r07qGIi2tX+6yIMaTDclSHBJeZSiUtze4PEbBUA2khKU5AVg8jjFEUrVq06i0+q7/AEOm+2s3LeKPdBLb428BkjczvZxzxiuZ2fJuk67Ozrxcbi67HhRAhpaltNlS2iVrU1yG8eRII+E9AOdaiNeIUO7aigztVuQEKnSlqhtRyHt3czvIcHMHlkY7RRFKNKiK23PULkBlrVNxu0B0zGvpYtJLamIpYUWVJKM7iVrA4i0kEL3k5AAxkXGesW22NWvUF4e0867JEi4TXnmlBY3OGjjpQHA3zcwvPMjG8elEUlSrpbospEWTNYafWUBLa1gKJWopRy8SCB5Vl1C4VcZM6xyJDr0x3i2/hvvNrQXGxNkbhVvAH5N34iMn5sc8Ut1z1AYjkly8zjeDbJS7lFK3iWVhhRB4RSEMFLm6ElPzD87OQRTRSoxmtags0cMQbteJb8u0JfluOOKkLQsPMpccaSQd1QbW6QhIwSE8q/J0xMexzzpPUN8uDSZMZM12Q46+IzRUeIppwoUrJGN8JJ3BzASRRFJ9K4/Ze++9EuSRcXbhCblBMV1brr2PgBUlLrg3nEg9vPByM8qURdhSlKIvl1tt1tTTqEuNrBCkqGQR3EVEO0LYbZrtxJumVotMw5JjkZjrPgBzR6ZHhUwUqenqZad3FGcKCenjnbwyDKo/qrTN80xcDCvdvdiuc9xRGUODvSociPKtPV7LzarbeYC4F1hMTIy/mbdRvDzHcfEc6gjaHsHeZ4k/Rr5ebHxGA+v4x4IWevkrHmas9He45fDL4T8vwq5V2eSPxReIfP8AKgqrN+yl/p3P/Wzn8Fmq2XGFMt0xyHPivRZLR3VtOoKVJPiDVk/ZS/07n/rZz+CzUl6INJkdQo7OMVWD0Kl2lKVTVbkpSlESlKURKUpREpSlESlKURKUpREpSlESlKURKUpREpSlESlKURKUpREpSlESlKURc/rPR2ntXQ/d71AQ6oDDb6Pheb/RV19DkeFcv7PluYtWlrxBjrcU21e5CElwgnCUtpGcAdgFKVvxvcaN7SdAQtF7GirYQNcFSRSlK0FvJSlKIlKUoiUpSiJSlKIlKUoiUpSiJSlKIlKUoiUpSiJSlKIlKUoi/9k="

# ── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.main .block-container{padding-top:1rem;padding-bottom:2rem;max-width:1400px;}
.logo-bar{display:flex;align-items:center;gap:14px;padding-bottom:14px;
    border-bottom:1px solid #eee;margin-bottom:18px;}
.logo-bar img{height:44px;object-fit:contain;}
.logo-bar h1{font-size:20px;font-weight:700;color:#1a1a1a;margin:0;}
.logo-bar .mbadge{margin-left:auto;background:#E1F5EE;color:#0F6E56;
    padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600;}
[data-testid="stSidebar"]{background:#1E293B;}
[data-testid="stSidebar"] *{color:#E2E8F0 !important;}
[data-testid="stSidebar"] label{color:#94A3B8 !important;font-size:11px !important;
    text-transform:uppercase;letter-spacing:.05em;font-weight:600;}
div[data-testid="metric-container"]{background:#F8F9FA;border:.5px solid #EBEBEB;
    border-radius:10px;padding:14px 18px;}
div[data-testid="metric-container"] label{font-size:10px !important;
    text-transform:uppercase;letter-spacing:.06em;color:#888 !important;font-weight:600;}
div[data-testid="metric-container"] [data-testid="metric-value"]{
    font-size:24px !important;font-weight:700 !important;color:#1a1a1a !important;}
.stTabs [data-baseweb="tab-list"]{gap:4px;border-bottom:1px solid #eee;}
.stTabs [data-baseweb="tab"]{font-size:12px;font-weight:500;padding:8px 14px;
    border-radius:4px 4px 0 0;color:#888;}
.stTabs [aria-selected="true"]{color:#3266ad !important;font-weight:600;
    background:white !important;border-bottom:2px solid #3266ad !important;}
.sec{font-size:13px;font-weight:600;color:#1a1a1a;margin-bottom:10px;
    padding-bottom:6px;border-bottom:.5px solid #eee;}
.infobox{background:#F0F7FF;border:.5px solid #C3DCFB;border-radius:8px;
    padding:10px 14px;font-size:12px;color:#185FA5;margin-bottom:14px;}
.sumrow{background:#F8F9FA;border-radius:8px;padding:10px 16px;
    font-size:11px;color:#555;margin:8px 0 14px 0;}
.insight-grid{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;}
.ic{flex:1;min-width:200px;border-radius:10px;padding:12px 14px;
    border-left:4px solid;font-size:12px;line-height:1.5;}
.ic-good{background:#F0FBF7;border-color:#1D9E75;}
.ic-warn{background:#FEF9EC;border-color:#BA7517;}
.ic-bad{background:#FEF0F0;border-color:#D85A30;}
.ic-info{background:#F0F7FF;border-color:#3266ad;}
.ic-title{font-weight:700;font-size:12px;margin-bottom:3px;}
.ic-text{color:#555;font-size:11px;}
hr.sub{border:none;border-top:.5px solid #eee;margin:14px 0;}
</style>""", unsafe_allow_html=True)

# ── CONSTANTS ────────────────────────────────────────────────────────────
PRODUCTIVE_STATUSES = [
    "Contacted - Interested", "Meeting Schedule",
    "Budget Constraint", "Deferred Interest"
]

CHART_COLORS = ["#3266ad","#1D9E75","#D85A30","#BA7517",
                "#8B5CF6","#0F6E56","#993556","#185FA5"]

STAGE_ORDER = ["Discovery/Teaser Demo","Demo","Technical Evaluation",
               "Negotiation/Review","CP wrt SOW","Closed Won"]

# 8 product groups with display names and Zoho category keywords
PRODUCT_GROUPS = {
    "LAB-LIMS":           ["lab - lims","lims"],
    "LAB-EMpro":          ["lab - empro","empro"],
    "Quality Assurance":  ["epiq","assureiq","docsiq","learniq","qcc",
                           "quality command","calibervi","quality - epiq",
                           "quality assurance"],
    "Manufacturing":      ["manufacturing","elog","ipqc","brm","wms",
                           "warehouse"],
    "D&I / DSG":          ["apqr","cpv","d&i","dsg","data analytics",
                           "digital quality"],
    "OTT-LAB":            ["ott-lab","ott lab"],
    "OTT-D&I":            ["ott-d&i","ott d&i","edisplay","ott"],
    "OTT-MFG":            ["ott-mfg","ott mfg"],
}

DEFAULT_TARGETS = {
    "LAB-LIMS":           0,
    "LAB-EMpro":          0,
    "Quality Assurance":  0,
    "Manufacturing":      0,
    "D&I / DSG":          0,
    "OTT-LAB":            0,
    "OTT-D&I":            0,
    "OTT-MFG":            0,
}

CHART_LAYOUT = dict(font_family="Inter", plot_bgcolor="white",
    paper_bgcolor="white", margin=dict(l=10,r=10,t=30,b=10),
    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
    height=280)

# ── HELPERS ──────────────────────────────────────────────────────────────
def normalize_region(r):
    r = str(r).strip()
    if not r or r == "nan": return "Unknown"
    if any(x in r for x in ["Guj","Gujarat","North"]): return "Guj & North"
    if "South" in r: return "South"
    if any(x in r for x in ["Maharashtra","Goa","Mah"]): return "Mah & Goa"
    if "APAC" in r: return "APAC"
    if "MENA" in r: return "MENA"
    return r

def map_product_group(product_category, product_group):
    """Map Zoho product category/group to one of the 8 user product groups."""
    pc = str(product_category).strip().lower()
    pg = str(product_group).strip().lower()
    combined = pc + " " + pg
    for group_name, keywords in PRODUCT_GROUPS.items():
        for kw in keywords:
            if kw in combined:
                return group_name
    return "Other"

def pct(num, den, d=1):
    return round(num / den * 100, d) if den > 0 else 0.0

def compute_metrics(df):
    total           = len(df)
    converted       = int(df["is_potential"].sum())
    prod_from_leads = int(df["is_productive"].sum())
    productive      = prod_from_leads + converted        # MQL total
    unproductive    = int(df["is_unproductive"].sum())
    pursuing        = int(df["is_pursuing"].sum())
    unclassified    = max(total - productive - unproductive - pursuing, 0)
    return dict(
        total=total, converted=converted,
        prod_from_leads=prod_from_leads,
        productive=productive,
        unproductive=unproductive,
        pursuing=pursuing,
        unclassified=unclassified,
        prod_pct=pct(productive, total),
        unprod_pct=pct(unproductive, total),
        conv_pct=pct(converted, productive),
    )

def breakdown_stats(df, col):
    rows = []
    for val in sorted(df[col].unique()):
        sub = df[df[col] == val]
        m   = compute_metrics(sub)
        rows.append({col: val, "Total": m["total"],
                     "Productive": m["productive"], "Prod %": m["prod_pct"],
                     "Unproductive": m["unproductive"], "Unprod %": m["unprod_pct"],
                     "Converted": m["converted"], "Conv %": m["conv_pct"]})
    return pd.DataFrame(rows).sort_values("Total", ascending=False).reset_index(drop=True)

def df_to_excel(sheets: dict):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        for name, df in sheets.items():
            df.to_excel(w, sheet_name=name[:31], index=False)
    return buf.getvalue()

def ic(icon, title, text, kind="info"):
    return f"""<div class="ic ic-{kind}">
        <div class="ic-title">{icon} {title}</div>
        <div class="ic-text">{text}</div></div>"""

def show_insights(cards):
    st.markdown('<div class="insight-grid">' + "".join(cards) + "</div>",
                unsafe_allow_html=True)

# ── CHART HELPERS ────────────────────────────────────────────────────────
def bar(df, x, y, colors=None, horizontal=False, height=280):
    kw = dict(text_auto=True, color_discrete_sequence=colors or CHART_COLORS)
    if horizontal:
        fig = px.bar(df, x=y, y=x, orientation="h", **kw)
        fig.update_xaxes(showgrid=True, gridcolor="#F0F0F0", zeroline=False)
        fig.update_yaxes(showgrid=False)
    else:
        fig = px.bar(df, x=x, y=y, **kw)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="#F0F0F0", zeroline=False)
    fig.update_traces(textfont_size=10, textposition="outside")
    fig.update_layout(**{**CHART_LAYOUT, "height": height})
    return fig

def donut(labels, values, colors=None, height=260):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker_colors=colors or CHART_COLORS, textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"))
    fig.update_layout(**{**CHART_LAYOUT, "height": height, "showlegend": True})
    return fig

def grouped_bar(categories, datasets, height=300):
    fig = go.Figure()
    for ds in datasets:
        fig.add_trace(go.Bar(name=ds["name"], x=categories, y=ds["data"],
            marker_color=ds["color"], text=ds["data"],
            textposition="outside", textfont_size=10))
    fig.update_layout(**{**CHART_LAYOUT, "height": height, "barmode": "group"})
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F0F0F0", zeroline=False)
    return fig

def trend(months, datasets, pct_axis=False, height=320):
    fig = go.Figure()
    pal = ["#3266ad","#1D9E75","#D85A30","#BA7517","#8B5CF6"]
    for i, ds in enumerate(datasets):
        fig.add_trace(go.Scatter(
            x=months, y=ds["data"], mode="lines+markers+text",
            name=ds["name"], line=dict(color=pal[i % len(pal)], width=2.5),
            marker=dict(size=8), text=ds["data"],
            textposition="top center", textfont_size=10))
    fig.update_layout(**{**CHART_LAYOUT, "height": height, "hovermode": "x unified"})
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F0F0F0", zeroline=False,
                     ticksuffix="%" if pct_axis else "")
    return fig

# ── LOAD EXCEL ───────────────────────────────────────────────────────────
def load_excel(file) -> pd.DataFrame:
    xl = pd.ExcelFile(file)
    sheets = xl.sheet_names

    def find_sheet(candidates, fallback=0):
        for s in sheets:
            if s.strip().lower() in candidates:
                return s
        return sheets[fallback] if fallback < len(sheets) else sheets[0]

    lead_sht = find_sheet(["lead","leads","lead data","lead report"], 0)
    pot_sht  = find_sheet(["potential","potentials","deals","opportunity"], 1)

    # ── Lead sheet ──────────────────────────────────────────────────────
    rl = xl.parse(lead_sht, dtype=str).fillna("")
    rl.columns = [c.strip().lower() for c in rl.columns]

    def gcol(df, *names, default=""):
        for n in names:
            if n in df.columns: return df[n]
        return pd.Series([default] * len(df))

    lead = pd.DataFrame()
    lead["full_name"]         = gcol(rl, "full name", "name")
    lead["region"]            = gcol(rl, "region", "territory")
    lead["product_category"]  = gcol(rl, "product category", "prod category")
    lead["product_group_raw"] = gcol(rl, "product group", "product")
    lead["lead_status"]       = gcol(rl, "lead status", "status")
    lead["type_of_source"]    = gcol(rl, "type of source")
    lead["lead_source"]       = gcol(rl, "lead source")
    lead["conversion_source"] = gcol(rl, "conversion source", "channel")
    lead["created_time"]      = gcol(rl, "created time", "date")
    lead["stage"]             = ""
    lead["sheet"]             = "Lead"

    # ── Potential sheet ─────────────────────────────────────────────────
    rp = xl.parse(pot_sht, dtype=str).fillna("")
    rp.columns = [c.strip().lower() for c in rp.columns]

    pot = pd.DataFrame()
    pot["full_name"]         = gcol(rp, "potential name", "account name", "name")
    pot["region"]            = gcol(rp, "region", "territory")
    pot["product_category"]  = gcol(rp, "prod category", "product category")
    pot["product_group_raw"] = gcol(rp, "product group", "product")
    pot["lead_status"]       = "Converted"
    pot["type_of_source"]    = gcol(rp, "type of source")
    pot["lead_source"]       = gcol(rp, "lead source")
    pot["conversion_source"] = gcol(rp, "conversion source", "channel")
    pot["created_time"]      = gcol(rp, "created time", "date")
    pot["stage"]             = gcol(rp, "stage", "pipeline stage")
    pot["sheet"]             = "Potential"

    # ── Combine ─────────────────────────────────────────────────────────
    cols = ["full_name","region","product_category","product_group_raw",
            "lead_status","type_of_source","lead_source","conversion_source",
            "created_time","stage","sheet"]
    df = pd.concat([lead[cols], pot[cols]], ignore_index=True).fillna("")

    # Normalize fields
    df["region"] = df["region"].apply(normalize_region)

    # Normalize conversion_source (strip spaces, title-case)
    df["conversion_source"] = df["conversion_source"].str.strip().str.title()

    # Map to 8 product groups
    df["product_group"] = df.apply(
        lambda r: map_product_group(r["product_category"], r["product_group_raw"]), axis=1)

    # Fix source: if type_of_source blank, use lead_source; event keyword → "Event"
    def fix_src(ts, ls):
        ts, ls = str(ts).strip(), str(ls).strip()
        if ls.lower().startswith("event") or ls.lower() == "event":
            return "Event"
        if ts in ("", "nan"):
            return ls if ls not in ("", "nan") else "Unknown"
        return ts
    df["type_of_source"] = df.apply(
        lambda r: fix_src(r["type_of_source"], r["lead_source"]), axis=1)

    # ── CORRECT CLASSIFICATIONS ─────────────────────────────────────────
    # Productive = specific statuses from Lead sheet
    df["is_productive"]   = df["lead_status"].isin(PRODUCTIVE_STATUSES)
    # Pursuing = Pursuing stage
    df["is_pursuing"]     = df["lead_status"] == "Pursuing"
    # Potential = from Potential sheet
    df["is_potential"]    = df["sheet"] == "Potential"
    # Unproductive = everything else from Lead sheet
    # (NOT productive, NOT pursuing, NOT potential)
    df["is_unproductive"] = (
        (~df["is_productive"]) &
        (~df["is_pursuing"]) &
        (~df["is_potential"])
    )
    return df

# ── SIDEBAR ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Lead Analytics")
    st.markdown("---")
    st.markdown("### 📂 Current Month Data")
    st.caption("Upload this month's Zoho Excel export")
    current_file = st.file_uploader("Current month (.xlsx)", type=["xlsx"],
        accept_multiple_files=False, key="cur",
        help="Must have Lead and Potential sheets")

    st.markdown("---")
    st.markdown("### 📅 Comparison Data")
    st.caption("Upload prior months for trend analysis")
    comparison_files = st.file_uploader("Prior month(s) (.xlsx)", type=["xlsx"],
        accept_multiple_files=True, key="cmp",
        help="Upload one or more prior month Excel files")

    st.markdown("---")
    region_filter  = []
    channel_filter = "All"
    if current_file:
        st.markdown("### 🔍 Filters")
        region_filter  = st.multiselect("Region",
            ["Guj & North","South","Mah & Goa","APAC","MENA"],
            default=[], placeholder="All regions")
        channel_filter = st.selectbox("Channel", ["All","Business","Marketing"])

    st.markdown("---")
    st.markdown("""<div style="font-size:11px;color:#64748B;line-height:1.8;">
    <b>Formulas</b><br>
    Total = Lead rows + Potential rows<br>
    Productive = Interested + Meeting + Budget + Deferred + Potential<br>
    Unproductive = All other Lead statuses (excl. Pursuing)<br>
    Conversion % = Potential / Productive MQL
    </div>""", unsafe_allow_html=True)

# ── WELCOME ──────────────────────────────────────────────────────────────
if not current_file:
    st.markdown(f"""
    <div style="text-align:center;padding:50px 20px;">
        <img src="data:image/jpeg;base64,{CALIBER_LOGO_B64}" style="height:60px;margin-bottom:20px;">
        <h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin-bottom:8px;">
            Lead Analytics Dashboard</h2>
        <p style="font-size:13px;color:#888;max-width:440px;margin:0 auto 24px;">
            Upload your monthly Zoho CRM Excel export from the sidebar.</p>
        <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
            <div style="background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;">
                <div style="font-size:20px;">⬆️</div>
                <div style="font-size:12px;font-weight:600;margin-top:6px;">Upload Excel</div>
                <div style="font-size:11px;color:#888;">Lead + Potential sheets</div>
            </div>
            <div style="background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;">
                <div style="font-size:20px;">📊</div>
                <div style="font-size:12px;font-weight:600;margin-top:6px;">Auto Dashboard</div>
                <div style="font-size:11px;color:#888;">All tabs fill instantly</div>
            </div>
            <div style="background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;">
                <div style="font-size:20px;">💡</div>
                <div style="font-size:12px;font-weight:600;margin-top:6px;">Smart Insights</div>
                <div style="font-size:11px;color:#888;">Auto alerts & trends</div>
            </div>
            <div style="background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;">
                <div style="font-size:20px;">📥</div>
                <div style="font-size:12px;font-weight:600;margin-top:6px;">Download</div>
                <div style="font-size:11px;color:#888;">Excel or PDF</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── LOAD DATA ─────────────────────────────────────────────────────────────
monthly_data = {}
try:
    label = current_file.name.replace(".xlsx","").replace("_"," ").replace("-"," ").strip()
    monthly_data[label] = load_excel(current_file)
    current_label = label
except Exception as e:
    st.error(f"⚠️ Could not load file: {e}")
    st.stop()

if comparison_files:
    for f in comparison_files:
        lbl = f.name.replace(".xlsx","").replace("_"," ").replace("-"," ").strip()
        if lbl == current_label: lbl += " (prior)"
        try: monthly_data[lbl] = load_excel(f)
        except Exception as e: st.error(f"⚠️ {f.name}: {e}")

df_all = monthly_data[current_label]

def apply_filters(df):
    out = df.copy()
    if region_filter:  out = out[out["region"].isin(region_filter)]
    if channel_filter != "All":
        out = out[out["conversion_source"] == channel_filter]
    return out

filtered = apply_filters(df_all)
m = compute_metrics(filtered)

# ── HEADER ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="logo-bar">
    <img src="data:image/jpeg;base64,{CALIBER_LOGO_B64}" alt="Caliber">
    <h1>Lead Analytics Dashboard</h1>
    <span class="mbadge">{current_label} &nbsp;·&nbsp; {m["total"]} leads</span>
</div>""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    "📋 Overview", "📡 Channel Performance", "🔗 Source Performance",
    "🗺️ Region Performance", "📦 Product Performance",
    "🔄 Funnel Movement", "📅 Period Comparison"])

# ═══════════════════════════════════════════════
# TAB 1  OVERVIEW
# ═══════════════════════════════════════════════
with t1:

    # ================= KPI CARDS =================
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Leads", m["total"])

    c2.metric(
        "Productive (MQL)",
        m["productive"],
        help="Interested + Meeting Schedule + Budget Constraint + Deferred Interest + All Potential Leads"
    )

    c3.metric(
        "Unproductive",
        m["unproductive"],
        help="All Lead statuses except Productive and Pursuing"
    )

    c4.metric(
        "Pursuing",
        m["pursuing"]
    )

    c5.metric(
        "Conversion %",
        f"{m['conv_pct']}%",
        help="Converted (Potential) ÷ Productive (MQL)"
    )

    # ================= INSIGHTS =================

    cards = []

    if m["unprod_pct"] > 50:
        cards.append(
            ic(
                "🔴",
                "High Unproductive Rate",
                f"{m['unprod_pct']}% of leads are unproductive. Review lead qualification.",
                "bad"
            )
        )
    else:
        cards.append(
            ic(
                "🟢",
                "Good Lead Quality",
                f"Only {m['unprod_pct']}% of leads are unproductive.",
                "good"
            )
        )

    if m["conv_pct"] >= 70:
        cards.append(
            ic(
                "🏆",
                "Excellent Conversion",
                f"{m['conv_pct']}% conversion achieved.",
                "good"
            )
        )

    elif m["conv_pct"] >= 40:
        cards.append(
            ic(
                "📈",
                "Healthy Conversion",
                f"{m['conv_pct']}% conversion. Continue regular follow-ups.",
                "info"
            )
        )

    else:
        cards.append(
            ic(
                "⚠️",
                "Low Conversion",
                f"Only {m['conv_pct']}% conversion. Review engagement quality.",
                "bad"
            )
        )

    if m["pursuing"] > 0:
        cards.append(
            ic(
                "🔄",
                "Active Opportunities",
                f"{m['pursuing']} leads are currently in Pursuing stage.",
                "info"
            )
        )

    show_insights(cards)

    st.markdown("<hr class='sub'>", unsafe_allow_html=True)

    # ================= CHARTS =================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "<div class='sec'>Lead Quality Distribution</div>",
            unsafe_allow_html=True
        )

        fig = donut(
            ["Converted", "Lead Productive", "Unproductive", "Pursuing"],
            [
                m["converted"],
                m["prod_from_leads"],
                m["unproductive"],
                m["pursuing"]
            ],
            colors=[
                "#1D9E75",
                "#3266ad",
                "#D85A30",
                "#BA7517"
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:

        st.markdown(
            "<div class='sec'>Conversion Contribution by Channel</div>",
            unsafe_allow_html=True
        )

        biz_c = filtered[
            (filtered["conversion_source"] == "Business") &
            (filtered["is_potential"])
        ].shape[0]

        mkt_c = filtered[
            (filtered["conversion_source"] == "Marketing") &
            (filtered["is_potential"])
        ].shape[0]

        fig = donut(
            ["Business", "Marketing"],
            [biz_c, mkt_c],
            colors=[
                "#185FA5",
                "#1D9E75"
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # ================= UNPRODUCTIVE BREAKDOWN =================

    st.markdown(
        "<div class='sec'>Unproductive Lead Breakdown</div>",
        unsafe_allow_html=True
    )

    ub = (
        filtered[
            filtered["is_unproductive"]
        ]["lead_status"]
        .value_counts()
        .reset_index()
    )

    ub.columns = ["Status", "Count"]

    fig = bar(
        ub,
        "Status",
        "Count",
        horizontal=True,
        colors=[
            "#F09595",
            "#ED93B1",
            "#EF9F27",
            "#AFA9EC",
            "#B4B2A9"
        ],
        height=220
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown("<hr class='sub'>", unsafe_allow_html=True)

    # ================= DOWNLOAD =================

    st.download_button(
        "📥 Download Full Report",
        data=df_to_excel({
            "Data": filtered[
                [
                    "full_name",
                    "region",
                    "product_group",
                    "lead_status",
                    "type_of_source",
                    "lead_source",
                    "conversion_source",
                    "stage"
                ]
            ]
        }),
        file_name=f"Caliber_Report_{current_label.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# ═══════════════════════════════════════════════
# TAB 2  CHANNEL PERFORMANCE
# ═══════════════════════════════════════════════
with t2:
    biz_df  = filtered[filtered["conversion_source"] == "Business"]
    mkt_df  = filtered[filtered["conversion_source"] == "Marketing"]
    biz_m   = compute_metrics(biz_df)
    mkt_m   = compute_metrics(mkt_df)

    cards = []
    if biz_m["conv_pct"] > mkt_m["conv_pct"]:
        gap = round(biz_m["conv_pct"] - mkt_m["conv_pct"], 1)
        cards.append(ic("💼","Business Converts Better",
            f"Business {biz_m['conv_pct']}% vs Marketing {mkt_m['conv_pct']}% — {gap}% gap.","good"))
    if mkt_m["unprod_pct"] > 60:
        cards.append(ic("⚠️","Marketing Unproductive Rate High",
            f"{mkt_m['unprod_pct']}% of marketing leads are unproductive.","bad"))
    show_insights(cards)
    st.markdown("<hr class='sub'>",unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>🔵 Business Channel</div>",unsafe_allow_html=True)
        b1,b2,b3,b4 = st.columns(4)
        b1.metric("Total",       biz_m["total"])
        b2.metric("Productive",  biz_m["productive"],  f"{biz_m['prod_pct']}%")
        b3.metric("Unproductive",biz_m["unproductive"])
        b4.metric("Converted",   biz_m["converted"],   f"Conv {biz_m['conv_pct']}%")
        biz_st = biz_df["lead_status"].value_counts().reset_index()
        biz_st.columns = ["Status","Count"]
        st.dataframe(biz_st, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("<div class='sec'>🟢 Marketing Channel</div>",unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Total",       mkt_m["total"])
        m2.metric("Productive",  mkt_m["productive"],  f"{mkt_m['prod_pct']}%")
        m3.metric("Unproductive",mkt_m["unproductive"])
        m4.metric("Converted",   mkt_m["converted"],   f"Conv {mkt_m['conv_pct']}%")
        mkt_st = mkt_df["lead_status"].value_counts().reset_index()
        mkt_st.columns = ["Status","Count"]
        st.dataframe(mkt_st, hide_index=True, use_container_width=True)

    st.markdown("<div class='sec'>Side-by-Side Comparison</div>",unsafe_allow_html=True)
    fig = grouped_bar(["Total","Productive","Unproductive","Converted"],
        [{"name":"Business","data":[biz_m["total"],biz_m["productive"],biz_m["unproductive"],biz_m["converted"]],"color":"#185FA5"},
         {"name":"Marketing","data":[mkt_m["total"],mkt_m["productive"],mkt_m["unproductive"],mkt_m["converted"]],"color":"#1D9E75"}])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    ch_df = pd.DataFrame([{"Channel":"Business",**biz_m},{"Channel":"Marketing",**mkt_m}])
    st.download_button("📥 Download Channel Data",
        data=df_to_excel({"Channel":ch_df}),
        file_name=f"Caliber_Channel_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ═══════════════════════════════════════════════
# TAB 3  SOURCE PERFORMANCE  (Marketing leads only)
# ═══════════════════════════════════════════════
with t3:
    st.markdown("""<div class="infobox">
    📌 <b>Marketing Channel Only</b> — Source performance based on Marketing leads only
    (conversion_source = Marketing)</div>""", unsafe_allow_html=True)

    src_df_base = filtered[filtered["conversion_source"] == "Marketing"]
    src_grp = (src_df_base.groupby("type_of_source")
               .agg(Total=("type_of_source","count"),
                    Productive=("is_productive","sum"),
                    Unproductive=("is_unproductive","sum"),
                    Pursuing=("is_pursuing","sum"),
                    Converted=("is_potential","sum"))
               .reset_index().rename(columns={"type_of_source":"Source"})
               .sort_values("Total",ascending=False))
    src_grp["Prod %"]   = src_grp.apply(lambda r: pct(r["Productive"],r["Total"]),axis=1)
    src_grp["Unprod %"] = src_grp.apply(lambda r: pct(r["Unproductive"],r["Total"]),axis=1)

    cards = []
    if len(src_grp) > 0:
        best = src_grp.sort_values("Prod %",ascending=False).iloc[0]
        worst = src_grp.sort_values("Unprod %",ascending=False).iloc[0]
        cards.append(ic("🌟","Best Quality Source",
            f"<b>{best['Source']}</b> — {best['Prod %']}% productive rate.","good"))
        if worst["Unprod %"] > 60:
            cards.append(ic("🔴","Highest Unproductive Source",
                f"<b>{worst['Source']}</b> — {worst['Unprod %']}% unproductive.","bad"))
    show_insights(cards)

    cols = st.columns(min(len(src_grp),5))
    for i,(_,row) in enumerate(src_grp.head(5).iterrows()):
        cols[i].metric(row["Source"], int(row["Total"]), f"Prod {row['Prod %']}%")
    st.markdown("<hr class='sub'>",unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>Lead Volume by Source</div>",unsafe_allow_html=True)
        fig = donut(src_grp["Source"].tolist(), src_grp["Total"].tolist(), colors=CHART_COLORS)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with col2:
        st.markdown("<div class='sec'>Productive % by Source</div>",unsafe_allow_html=True)
        fig = bar(src_grp.sort_values("Prod %"),"Source","Prod %",
                  horizontal=True,colors=CHART_COLORS)
        fig.update_xaxes(ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    st.markdown("<div class='sec'>Detailed Source Performance</div>",unsafe_allow_html=True)
    st.dataframe(src_grp[["Source","Total","Productive","Prod %","Unproductive","Unprod %","Converted","Pursuing"]],
                 hide_index=True, use_container_width=True)
    st.download_button("📥 Download Source Data",
        data=df_to_excel({"Source":src_grp}),
        file_name=f"Caliber_Source_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ═══════════════════════════════════════════════
# TAB 4  REGION PERFORMANCE  (Marketing only)
# ═══════════════════════════════════════════════
with t4:
    st.markdown("""<div class="infobox">
    📌 <b>Marketing Channel Only</b></div>""", unsafe_allow_html=True)
    mkt_only = filtered[
    filtered["conversion_source"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
    == "MARKETING"
].copy()
    rg_df    = breakdown_stats(mkt_only, "region")

    cards = []
    if len(rg_df) > 0:
        best  = rg_df.sort_values("Prod %",ascending=False).iloc[0]
        worst = rg_df.sort_values("Unprod %",ascending=False).iloc[0]
        cards.append(ic("🌍","Best Performing Region",
            f"<b>{best['region']}</b> — {best['Prod %']}% productive rate.","good"))
        if worst["Unprod %"] > 70:
            cards.append(ic("🔴","Region Needs Attention",
                f"<b>{worst['region']}</b> — {worst['Unprod %']}% unproductive.","bad"))
    show_insights(cards)

    cols = st.columns(min(len(rg_df),5))
    for i,(_,row) in enumerate(rg_df.head(5).iterrows()):
        cols[i].metric(row["region"],int(row["Total"]),f"Prod {row['Prod %']}%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>Region Distribution</div>",unsafe_allow_html=True)
        fig = bar(rg_df,"region","Total",colors=["#1D9E75"])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with col2:
        st.markdown("<div class='sec'>Productive % by Region</div>",unsafe_allow_html=True)
        fig = bar(rg_df.sort_values("Prod %"),"region","Prod %",horizontal=True,colors=CHART_COLORS)
        fig.update_xaxes(ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    st.markdown("<div class='sec'>Region-Wise Performance (Marketing Only)</div>",unsafe_allow_html=True)
    st.dataframe(rg_df.rename(columns={"region":"Region"}),hide_index=True,use_container_width=True)
    st.download_button("📥 Download Region Data",
        data=df_to_excel({"Region":rg_df}),
        file_name=f"Caliber_Region_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# # ═══════════════════════════════════════════════
# ═══════════════════════════════════════════════
# TAB 5 - PRODUCT PERFORMANCE
# ═══════════════════════════════════════════════
with t5:

    st.markdown("""
    <div class="infobox">
    📌 <b>Marketing Channel Performance</b><br>
    Product Performance is calculated using only records where
    <b>Conversion Source = Marketing</b>.
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Marketing Data Only
    # ----------------------------------------------------------
    mkt_only = filtered[
        filtered["conversion_source"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper() == "MARKETING"
    ].copy()

    # ----------------------------------------------------------
    # Editable Targets
    # ----------------------------------------------------------
    st.markdown(
        "<div class='sec'>📎 Monthly Product Targets</div>",
        unsafe_allow_html=True
    )

    target_cols = st.columns(4)

    targets = {}

    pg_list = list(PRODUCT_GROUPS.keys())

    for i, pg in enumerate(pg_list):

        with target_cols[i % 4]:

            targets[pg] = st.number_input(
                pg,
                min_value=0,
                value=DEFAULT_TARGETS.get(pg, 0),
                step=1,
                key=f"target_{pg}"
            )

    st.markdown("<hr class='sub'>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Product Wise Calculation
    # ----------------------------------------------------------

    productive_status = [
        "Contacted - Interested",
        "Meeting Schedule",
        "Budget Constraint",
        "Deferred Interest"
    ]

    rows = []

    for pg in pg_list:

        sub = mkt_only[
            mkt_only["product_group"] == pg
        ].copy()

        lead_df = sub[sub["is_potential"] == False]

        potential_df = sub[sub["is_potential"] == True]

        target = targets[pg]

        received = len(lead_df)

        productive_leads = lead_df[
            lead_df["lead_status"].isin(productive_status)
        ].shape[0]

        converted = len(potential_df)

        productive = productive_leads + converted

        unproductive = lead_df[
            ~lead_df["lead_status"].isin(
                productive_status + ["Pursuing"]
            )
        ].shape[0]

        remaining = max(target - received, 0)

        rows.append({

            "Product Group": pg,

            "Target": target,

            "Actual Leads": received,

            "Remaining Target": remaining,

            "Productive": productive,

            "Prod %": pct(productive, received),

            "Unproductive": unproductive,

            "Unprod %": pct(unproductive, received),

            "Converted": converted,

            "Conv %": pct(converted, productive)

        })

    pg_table = pd.DataFrame(rows)

    # ----------------------------------------------------------
    # KPI
    # ----------------------------------------------------------

    total_target = pg_table["Target"].sum()

    total_actual = pg_table["Actual Leads"].sum()

    total_converted = pg_table["Converted"].sum()

    overall = pct(total_actual, total_target)

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total Target", total_target)

    k2.metric("Actual Leads", total_actual)

    k3.metric("Achievement", f"{overall}%")

    k4.metric("Converted", total_converted)

    st.markdown("<hr class='sub'>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Charts
    # ----------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            "<div class='sec'>Target vs Actual Leads</div>",
            unsafe_allow_html=True
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name="Target",
                x=pg_table["Product Group"],
                y=pg_table["Target"]
            )
        )

        fig.add_trace(
            go.Bar(
                name="Actual",
                x=pg_table["Product Group"],
                y=pg_table["Actual Leads"]
            )
        )

        fig.update_layout(
            **{**CHART_LAYOUT,
               "barmode": "group",
               "height": 300}
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with c2:

        st.markdown(
            "<div class='sec'>Productive vs Unproductive %</div>",
            unsafe_allow_html=True
        )

        fig2 = go.Figure()

        fig2.add_trace(
            go.Bar(
                name="Productive %",
                x=pg_table["Product Group"],
                y=pg_table["Prod %"]
            )
        )

        fig2.add_trace(
            go.Bar(
                name="Unproductive %",
                x=pg_table["Product Group"],
                y=pg_table["Unprod %"]
            )
        )

        fig2.update_layout(
            **{**CHART_LAYOUT,
               "barmode": "group",
               "height": 300}
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # ----------------------------------------------------------
    # Conditional Formatting
    # ----------------------------------------------------------

    def highlight(row):

        style = [""] * len(row)

        cols = list(row.index)

        if row["Actual Leads"] < row["Target"]:

            style[cols.index("Actual Leads")] = \
                "background-color:#FDE2E1;color:#C62828;font-weight:bold;"

        if row["Prod %"] < 25:

            style[cols.index("Prod %")] = \
                "background-color:#FFF3CD;color:#9A6700;font-weight:bold;"

        if row["Conv %"] < 60:

            style[cols.index("Conv %")] = \
                "background-color:#FDE2E1;color:#C62828;font-weight:bold;"

        return style

    st.markdown(
        "<div class='sec'>Product Performance Summary</div>",
        unsafe_allow_html=True
    )

    st.dataframe(
        pg_table.style.apply(highlight, axis=1),
        hide_index=True,
        use_container_width=True
    )

    # ----------------------------------------------------------
    # Download
    # ----------------------------------------------------------

    st.download_button(
        "📥 Download Product Performance",
        data=df_to_excel({
            "Product Performance": pg_table
        }),
        file_name=f"Product_Performance_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# ═══════════════════════════════════════════════
# TAB 6  FUNNEL MOVEMENT
# ═══════════════════════════════════════════════
with t6:
    potentials = filtered[filtered["is_potential"] & (filtered["stage"] != "")]
    sc = potentials["stage"].value_counts().reset_index()
    sc.columns = ["Stage","Count"]

    cards = []
    total_pot = len(potentials)
    if total_pot > 0:
        demo_c  = sc[sc["Stage"].str.contains("Demo",na=False)]["Count"].sum()
        negot_c = sc[sc["Stage"].str.contains("Negot",na=False)]["Count"].sum()
        won_c   = sc[sc["Stage"]=="Closed Won"]["Count"].sum() if "Closed Won" in sc["Stage"].values else 0
        early   = sc[sc["Stage"].isin(["Discovery/Teaser Demo","Demo"])]["Count"].sum()
        late    = sc[sc["Stage"].isin(["Negotiation/Review","CP wrt SOW","Closed Won"])]["Count"].sum()
        if demo_c > 0:
            cards.append(ic("📋","Strong Demo Pipeline",
                f"{demo_c} leads in Demo stage. Ensure capacity to move them forward.","info"))
        if negot_c > 0:
            cards.append(ic("🤝","Leads in Negotiation",
                f"{negot_c} near conversion — prioritise attention here.","good"))
        if won_c > 0:
            cards.append(ic("🏆","Closed Won",f"{won_c} deal(s) closed!","good"))
        if early > late * 2:
            cards.append(ic("⚠️","Funnel Top-Heavy",
                f"Most leads early ({early}) vs late ({late}). Focus on mid-funnel movement.","warn"))
    show_insights(cards)
    st.markdown("<hr class='sub'>",unsafe_allow_html=True)

    fc = st.columns(len(STAGE_ORDER))
    for i, stage in enumerate(STAGE_ORDER):
        cnt = sc[sc["Stage"]==stage]["Count"].values
        fc[i].metric(stage.split("/")[0], int(cnt[0]) if len(cnt) else 0)

    col1, col2 = st.columns(2)
    order_map = {s:i for i,s in enumerate(STAGE_ORDER)}
    sc["ord"] = sc["Stage"].map(lambda x: order_map.get(x,99))
    sc_ord = sc.sort_values("ord")
    stage_colors = ["#B5D4F4","#3266ad","#BA7517","#D85A30","#993556","#1D9E75"]
    with col1:
        st.markdown("<div class='sec'>Stage Distribution</div>",unsafe_allow_html=True)
        fig = bar(sc_ord,"Stage","Count",horizontal=True,
                  colors=stage_colors[:len(sc_ord)])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with col2:
        st.markdown("<div class='sec'>Stage Donut</div>",unsafe_allow_html=True)
        fig = donut(sc_ord["Stage"].tolist(),sc_ord["Count"].tolist(),
                    colors=stage_colors[:len(sc_ord)])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    st.markdown("<div class='sec'>All Potential Leads</div>",unsafe_allow_html=True)
    pot_show = potentials[["full_name","region","product_group","lead_status","stage","conversion_source"]].copy()
    pot_show.columns = ["Name","Region","Product","Status","Stage","Channel"]
    st.dataframe(pot_show, hide_index=True, use_container_width=True)
    st.download_button("📥 Download Funnel Data",
        data=df_to_excel({"Funnel":pot_show}),
        file_name=f"Caliber_Funnel_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ═══════════════════════════════════════════════
# TAB 7  PERIOD COMPARISON + TRENDS
# ═══════════════════════════════════════════════
with t7:
    if len(monthly_data) < 2:
        st.markdown("""<div class="infobox">
        💡 Upload prior month files from the sidebar to activate trend analysis.
        </div>""", unsafe_allow_html=True)

    summary_rows = []
    for lbl in sorted(monthly_data.keys()):
        mm = compute_metrics(monthly_data[lbl])
        summary_rows.append({"Month":lbl,"Total":mm["total"],
            "Productive":mm["productive"],"Prod %":mm["prod_pct"],
            "Unproductive":mm["unproductive"],"Unprod %":mm["unprod_pct"],
            "Converted":mm["converted"],"Conv %":mm["conv_pct"],
            "Pursuing":mm["pursuing"]})
    summary = pd.DataFrame(summary_rows)
    months  = summary["Month"].tolist()

    if len(summary) >= 2:
        cr, pr = summary.iloc[-1], summary.iloc[-2]
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Leads",   int(cr["Total"]),      int(cr["Total"]-pr["Total"]))
        c2.metric("Productive",    int(cr["Productive"]),  int(cr["Productive"]-pr["Productive"]))
        c3.metric("Unproductive",  int(cr["Unproductive"]),int(-(cr["Unproductive"]-pr["Unproductive"])))
        c4.metric("Converted",     int(cr["Converted"]),   int(cr["Converted"]-pr["Converted"]))
        c5.metric("Conversion %",  f"{cr['Conv %']}%",     f"{round(cr['Conv %']-pr['Conv %'],1)}%")

        cards = []
        if cr["Total"]-pr["Total"] > 0:
            cards.append(ic("📈","Volume Growing",
                f"Total leads up {int(cr['Total']-pr['Total'])} vs last period.","good"))
        elif cr["Total"]-pr["Total"] < 0:
            cards.append(ic("📉","Volume Declining",
                f"Total leads down {abs(int(cr['Total']-pr['Total']))} vs last period.","bad"))
        if cr["Conv %"]-pr["Conv %"] > 0:
            cards.append(ic("🚀","Conversion Improving",
                f"Conversion up {round(cr['Conv %']-pr['Conv %'],1)}%.","good"))
        elif cr["Conv %"]-pr["Conv %"] < -5:
            cards.append(ic("⚠️","Conversion Dropped",
                f"Conversion fell {abs(round(cr['Conv %']-pr['Conv %'],1))}%.","warn"))
        show_insights(cards)
        st.markdown("<hr class='sub'>",unsafe_allow_html=True)

    st.markdown("<div class='sec'>📈 Volume Trend over Months</div>",unsafe_allow_html=True)
    fig = trend(months,
        [{"name":"Total","data":summary["Total"].tolist()},
         {"name":"Productive","data":summary["Productive"].tolist()},
         {"name":"Unproductive","data":summary["Unproductive"].tolist()},
         {"name":"Converted","data":summary["Converted"].tolist()}],height=340)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    st.markdown("<div class='sec'>📈 Rate Trend over Months</div>",unsafe_allow_html=True)
    fig2 = trend(months,
        [{"name":"Productive %","data":summary["Prod %"].tolist()},
         {"name":"Unproductive %","data":summary["Unprod %"].tolist()},
         {"name":"Conversion %","data":summary["Conv %"].tolist()}],
        pct_axis=True,height=300)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

    if len(summary) >= 2:
        st.markdown("<div class='sec'>📊 Month-on-Month Comparison</div>",unsafe_allow_html=True)
        l2 = summary.tail(2)
        fig3 = grouped_bar(["Total","Productive","Unproductive","Converted","Pursuing"],
            [{"name":l2.iloc[-1]["Month"],
              "data":[int(l2.iloc[-1][c]) for c in ["Total","Productive","Unproductive","Converted","Pursuing"]],
              "color":"#3266ad"},
             {"name":l2.iloc[-2]["Month"],
              "data":[int(l2.iloc[-2][c]) for c in ["Total","Productive","Unproductive","Converted","Pursuing"]],
              "color":"#B4B2A9"}],height=300)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

    st.markdown("<div class='sec'>All Months Summary</div>",unsafe_allow_html=True)
    st.dataframe(summary, hide_index=True, use_container_width=True)
    st.download_button("📥 Download Comparison Report",
        data=df_to_excel({"Period Comparison":summary}),
        file_name="Caliber_Period_Comparison.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
