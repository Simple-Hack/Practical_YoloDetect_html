#include<stdlib.h>
#include<stdio.h>
#include<string.h>
//定义结构体
typedef struct {
	unsigned int weight;
	unsigned int parent, lchild, rchild;
}HTNode, * HuffmanTree;

typedef char** HuffmanCode;


//从TH中选择最小的两个节点，并将坐标返还给s1和s2
void Select(HuffmanTree& TH, int i, int* s1, int* s2) {
	int x, y;
	int number = 0;

    //找到父母节点为空的节点的个数，用来创建数组，决定数组的大小
	for (x = 1; x <= i; x++) {
		if (TH[x].parent == 0)
			number++;
	}
    //创建数组，用来保存父母节点为空的节点的值，为排序做准备
	int* T = (int*)malloc(number * sizeof(int));
    //将父母节点不为空的值赋值给数组
	for (x = 0, y = 1; x < number && y <= i;) {
        //相等就直接赋值
		if (TH[y].parent == 0) {
			T[x] = TH[y].weight;
			x++;
			y++;
		}
		else {
            //否则继续查找TH，即y++
			y++;
			continue;
		}
	}
    //此时，开始对数组元素排序
	for (x = 0; x < number - 1; x++) {
		for (y = x + 1; y < number; y++) {
			if (T[x] < T[y]) {
				continue;
			}
			else {
				int a = T[x];
				T[x] = T[y];
				T[y] = a;
			}
		}
	}
    //从小到大排序，故最小的为前两个数组元素
	int ss1 = T[0];
	int ss2 = T[1];
    //此时要逆着通过权值来找到对应的节点所在的位置
	if (ss1 != ss2) {
        //不相等直接一个一个遍历即可，找到权值一样的将坐标赋给s1和s2
		for (x = 1; x <= i; x++) {
			if (TH[x].parent == 0) {
				if (TH[x].weight == ss1) {
					*s1 = x;
				}
				else if (TH[x].weight == ss2) {
					*s2 = x;
				}
			}
		}
	}
    //如果两个相等，则要分开查找
	else if (ss1 == ss2) {
		int jishu = 0;
        //查找到第一个就截断，随便赋给s1或者s2
		for (x = 1; x <= i; x++) {
			if (TH[x].parent == 0) {
				if (TH[x].weight == ss1) {
					*s1 = x;
					jishu++;
					break;
				}
			}
		}
        //接着继续遍历查找，赋给另一个
		for (; x <= i; x++) {
			if (TH[x].parent == 0) {
				if (TH[x].weight == ss1) {
					*s2 = x;
				}
			}
		}
	}
    //检查输出结果是否正确
	for (int i = 0; i < number; i++) {
		printf("%d ", T[i]);

	}
	printf("s1==%d\ns2==%d\n", ss1, ss2);
	putchar('\n');
	free(T);
}
//开始编码
void HuffmanCoding(HuffmanTree& HT, HuffmanCode& HC, unsigned int* w, int n) {
	if (n <= 1)
		return;
	//满二叉树的顶点数就是2的n次方—1
	int m = 2 * n - 1;
	int s1, s2;
	//建立二叉树，申请内存
	HT = (HuffmanTree)malloc((m + 1) * sizeof(HTNode));
	//从第一个开始
	HuffmanTree  p = HT + 1;
	//初始化前 n 个节点，将字符频率赋值给它们的权值字段，并设置父母和子节点索引为0。
	int i;
	for (i = 1; i <= n; i++, p++, w++) {
		*p = { *w,0,0,0 };
	}
	//初始化剩余的 m - n 个节点，这些节点在后续过程中作为合并节点使用。
	for (; i <= m; i++, p++) {
		*p = { 0,0,0,0 };
	}
	//通过循环，从 n+1 到 m
	//每次调用 Select 函数找出当前未被合并且权值最小的两个节点（以它们的索引表示）
	//然后合并这两个节点形成新的父节点，并更新树结构中的关系和权值。
	for (i = n + 1; i <= m; i++) {
		Select(HT, i - 1, &s1, &s2);
		HT[s1].parent = i;
		HT[s2].parent = i;
		HT[i].lchild = s1;
		HT[i].rchild = s2;
		HT[i].weight = HT[s1].weight + HT[s2].weight;

	}
	//分配内存空间来存储哈夫曼编码结果 HC，即一个指向字符编码字符串的指针数组。
	if (!(HC = (HuffmanCode)malloc((n + 1) * sizeof(char*))))
		return;
	//为每一个字符生成哈夫曼编码
	char* cd = (char*)malloc(n * sizeof(char));
	cd[n - 1] = '\0';
	for (i = 1; i <= n; i++) {
		int start = n - 1;
		int c;
		int f;
		//对于每一个字符，从叶子节点到根节点遍历其路径
		
		for (c = i, f = HT[i].parent; f != 0; c = f, f = HT[f].parent) {
			//将经过左孩子的路径记为 '0'，
			if (HT[f].lchild == c)
				cd[--start] = '0';
			//右孩子的路径记为 '1'
			else {
				cd[--start] = '1';
			}
		}
		//随着深度的递增，编码长度也提升，也就是n-start
		HC[i] = (char*)malloc((n - start) * sizeof(char));
		//将从临时缓冲区 cd 开始的有效编码（即从索引 start 到字符串结束）复制到刚刚分配给 HC[i] 的内存空间中
		strcpy_s(HC[i], sizeof(char*), &cd[start]);
	}

	putchar('\n');
	for (int i = 1; i < 8; i++) {
		printf("%s ", HC[i]);
	}
	free(cd);
}

int main(void) {
	//示例
	unsigned int w[7] = { 4,2,7,6,8,10,12 };
	HuffmanTree HT;
	HuffmanCode HC;
	HuffmanCoding(HT, HC, w, 7);


	return 0;
}