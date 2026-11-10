import subprocess, textwrap, pathlib, sys
from xml.sax.saxutils import escape as e
NAVY, CREAM, YEL, GREY, SUB = "#0B1220", "#F2EEE6", "#F5B700", "#3A4558", "#AEB6C4"
W,H=1080,1350; JP="Noto Sans CJK JP, sans-serif"
out=pathlib.Path(sys.argv[1])
def grid(y0=1130):
    s=""
    for i,x in enumerate(range(140,1000,170)):
        c=YEL if i==2 else GREY; yy=y0+(30 if i%2 else 0)
        s+=f'<path d="M{x} {yy+80} V{yy} H{x+100} V{yy+80}" fill="none" stroke="{c}" stroke-width="10"/>'
    return s
def base(n,inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{NAVY}"/>'
      f'<text x="80" y="130" font-family="Inter" font-weight="700" font-size="44" fill="{CREAM}">Eurogrid</text>'
      f'<text x="1000" y="130" text-anchor="end" font-family="Inter" font-size="34" fill="{SUB}">{n}/4</text>'
      + inner + grid() + f'<text x="540" y="1290" text-anchor="middle" font-family="Inter" font-size="30" fill="{SUB}">@eurogrid_jp</text></svg>')
def lines(txt,x,y,size,n,fill=CREAM,lh=None,weight="400"):
    lh=lh or int(size*1.5); s=""; i=0
    for para in txt.split("\n"):
        for ln in (textwrap.wrap(para,n) or [""]):
            s+=f'<text x="{x}" y="{y+i*lh}" font-family="{JP}" font-weight="{weight}" font-size="{size}" fill="{fill}">{e(ln)}</text>'; i+=1
    return s
cards=[
 lines("カタールGP｜決勝のあと",80,300,40,30,YEL)+lines("小椋藍、\n4位でも\n「うれしくない」",80,460,96,10,CREAM,130,"700")+lines("何が足りなかったのか、本人の言葉から",80,900,40,22,SUB),
 lines("レースの流れ",80,300,56,20,YEL,weight="700")+lines("序盤：ザルコとの争いに時間を使い、KTMのアコスタとバスティアニーニに前に行かれる\n15周目：バスティアニーニを抜く\n17周目：アコスタを抜く\n最後：マルケスとチームメイトのR.フェルナンデスを追うが届かず。トップから4秒885差の4位",80,420,44,21,CREAM,66),
 lines("本人の言葉",80,300,56,20,YEL,weight="700")+'<rect x="80" y="360" width="10" height="560" fill="#F5B700"/>'+lines("「ザルコと戦いすぎた。お互い考え方がちがったから、あんなに争うことになった」\n「終盤のペースは悪くなかった。タイヤはうまく管理できた」\n「よかったところもあるけど、悪かったところのほうが多い」",120,430,44,19,CREAM,66)+lines("出典：Speedweek",120,1020,30,30,SUB),
 lines("Eurogridの見方",80,300,56,20,YEL,weight="700")+lines("前日は「7位か8位が最大かも」と\n話していた。それを3つ上回っても、\n満足していない。\n\nランキングは5位で、残りは2戦。\nポルトガル（11/20〜22）と\nバレンシア（11/27〜29）。\n来季はヤマハへ移る。\n本人が見ているのは、\nもっと上の順位のようだ。",80,400,42,40,CREAM,60)+lines("出典：Speedweek、Marca",80,1075,30,30,SUB),
]
for i,c in enumerate(cards,1):
    svg=out/f"c{i}.svg"; svg.write_text(base(i,c),encoding="utf-8")
    subprocess.run(["rsvg-convert","-o",str(out/f"c{i}.png"),str(svg)],check=True)
    from PIL import Image; Image.open(out/f"c{i}.png").convert("RGB").save(out/f"c{i}.jpg",quality=92); (out/f"c{i}.png").unlink(); svg.unlink()
print("ok")
