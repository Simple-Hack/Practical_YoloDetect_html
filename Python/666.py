class Solution:
    def finalString(self, s: str) -> str:
        str_len=len(s)

        hashMap={}

        for i in range(str_len):
            if s[i]=='i':
               j=i+1
               if j >= str_len:
                   break
               else:
                   while j < str_len and s[j]!='i':
                       j+=1
            hashMap[i]=j
        
        for j in range(str_len):
            if j in hashMap:
                if j+1 >= str_len:
                    continue
                else:
                    if hashMap[j]==j+1:
                        j+=1
                        continue
                    else:
                        begin=str_len-i+1
                        end=begin+hashMap[i]-i-2
                        for k in range(end,begin+1,-1):
                            print(s[k],end='')
                        j+=end-begin+1
            else:
                print(s[j],end='')






               
                