hangCan=["Canh","Tân","Nhâm","Quý","Giáp","Ất","Bính","Đinh","Mậu","Kỷ"]
hangChi=["Thân","Dậu","Tuất","Hợi","Tý","Sửu","Dần","Mão","Thìn","Tị","Ngọ","Mùi"]
menh=["Mộc","Thủy","Kim","Hỏa","Mộc","Thổ","Kim","Hỏa","Thủy","Thổ","Kim","Mộc","Thủy","Thổ","Hỏa"]

def year(n):
    res=str(n)+","

    res+=hangCan[n%10]
    res+=" "

    res+=hangChi[n%12]
    res+=","

    if (n%2==1): n-=1
    n=int(n/2)
    res+=menh[n%15]

    return res

print(year(2060))
