
def altjoch (distfloorknee):
    dist=(47-distfloorknee)
    if(dist<0):
        print("a cadeira esta muito alta abaixe ela em:", -1*dist, "cm")
    elif(dist==0):
        print("a cadeira está numa ótima altura")
    else:
        print("a cadeira está muito baixa suba ela em:", dist, "cm")

