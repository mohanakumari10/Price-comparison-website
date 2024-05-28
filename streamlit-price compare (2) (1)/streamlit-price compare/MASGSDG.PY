
n=int(input())
m=int(input())
for i in range(n,m+1):
    if((i%2!=0 and i%3!=0) and (i%5!=0 and i%7!=0)):
        print()
    print(i)