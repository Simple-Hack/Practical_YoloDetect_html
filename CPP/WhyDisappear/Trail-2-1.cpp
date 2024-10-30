#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define LEN 255
char src[LEN];
int i;
bool flag;
void E();
void T();
void G();
void F();
void S();

int main() {
	while (true) {
		flag = true;
		system("cls"); //win
		printf("-------某文法如下---------\n");
		printf("E->TG \n");
		printf("T->FS \n");
		printf("G->+TG|-TG|ε \n");
		printf("F->i|(E) \n");
		printf("S->*FS|/FS|ε\n");
		printf("请输入字符串，以#结束，例如(i+i)*i# 退出可输入exit\n");
		printf("字符串只能包含 i + - * / (  ) 等终结符\n");
		scanf("%s", &src);
		if (strcmp(src, "exit") == 0) break;
		i = 0;
		E();
		if (src[i]=='#'&&flag == true) printf("语法正确\n");
		else	printf("语法错误\n");
		system("pause");
	}
	return 0;
}
void E() {
	printf("\t进入E()函数\n");
	printf("E->TG \n");
	T();
	G();
}
void T() {
	printf("\t进入T()函数\n");
	printf("T->FS \n");
	F();
	S();
}
void G() {
	printf("\t进入G()函数\n");
	if (src[i] == '+') {
		printf("\t\t\t匹配+ \n");
		printf("G->+TG \n");
		i++;
		T();
		G();
	}
	else if (src[i] == '-') {
		printf("\t\t\t匹配- \n");
		printf("G->-TG \n");
		i++;
		T();
		G();
	}
	else
		printf("G→ε，忽略\n");
}

void F() {
	printf("\t进入F()函数\n");
	if (src[i] == '(') {
		printf("\t\t\t匹配( \n");
		printf("F->(E) \n");
		i++;
		E();
		if (src[i] == ')'){
			printf("\t\t\t匹配) \n");
			i++;
		}
		else flag = false;
	}
	else if (src[i] == 'i')
	{
		printf("\t\t\t匹配i \n");
		printf("F->i \n");
		i++;
	}
	else flag = false;
}
void S() {
	printf("\t进入S()函数\n");
	if (src[i] == '*') {
		printf("\t\t\t匹配*\n");
		i++;
		printf("S->*FS \n");
		F();
		S();
	}
	else if (src[i] == '/') {
		printf("\t\t\t匹配/  \n");
		i++;
		printf("S->/FS \n");
		F();
		S();
	}
	else
		printf("S→ε，忽略\n");
}
