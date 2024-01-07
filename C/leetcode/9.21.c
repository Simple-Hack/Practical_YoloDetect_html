#include <stdio.h>
static trap(int* height, int heightSize){
    int max_height=0;
    for(int i=0;i<heightSize; i++)
    {
            if(height[i] > max_height)
            {
                max_height = height[i];
            }
    }
    int ge_zi[max_height][heightSize];
    int yu_di[max_height];
    for(int i=0;i<max_height;i++){
        yu_di[i] = 0;
    }
    for(int i=0;i<heightSize;i++){
        for(int j=max_height-1;j>=0;j--){
            int temp = height[i];
            while(temp>0){
                ge_zi[j][i]=1;
                temp--;
            }
        }
    }
    printf("max_height=%d\n",max_height);
    for(int i=0;i<max_height;i++){
        for(int j=0;j<heightSize;j++){
            printf("%d  ",ge_zi[i][j]);
        }
        printf("\n------------\n");
    }
    for(int i=0;i<max_height;i++){
        for(int j=0;j<heightSize;j++){
            if(ge_zi[i][j]==1)
            {
                for(int k=j+1;k<heightSize;k++){
                    if(ge_zi[i][k]==1){
                        yu_di[i]+=k-j-1;
                        printf("yu_di[%d]=%d\n",i,yu_di[i]);
                        j=k;
                    }
                }
            }
        }
    }
    int num_yu_di=0;
    for(int i=0;i<max_height;i++){
        num_yu_di+=yu_di[i];
    }
    return num_yu_di;
}        
int main(){
    int size=12;
    int height[size];
    height[0]=0;
    height[1]=1;
    height[2]=0;
    height[3]=2;
    height[4]=1;
    height[5]=0;
    height[6]=1;
    height[7]=3;
    height[8]=2;
    height[9]=1;
    height[10]=2;
    height[11]=1;
    int num=trap(height,size);
    printf("结果为：%d\n",num);
    return 0;
}