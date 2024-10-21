#include<iostream>
#include<cctype>
#include<string>
#include <string.h>

//判断字符串是否包含连续两个a或两个b的串，字符串由a和b构成。有0-3共4状态

int DFA[4][2] = { 
	{ 1,2 },
	{ 3,2 },
	{ 1,3 },
	{ 3,3 } };
int firstState = 0; //初态
char charset[2] = { 'a','b' };//字符集
int endState[1] = { 3 }; //终态集

int run(int begin, char * inputStr) {
	int state = firstState;
	for (int i = 0; i<strlen(inputStr); i++) {
		switch (inputStr[i]) {
			case 'a': state = DFA[state][0]; break;
			case 'b': state = DFA[state][1]; break;
			default:  state = -1;
		}
		if (state == -1) break;
	}
	return state;
}
//判断产生的状态state是否在终态集
int isInEndState(int state) {
	for (int i = 0; i<1; i++)
		if (endState[i] == state)  return 1;
	return 0;
}

int main(int argc, char * args[]) {
	char inputStr[100];
	printf("请输入字符串\n");
	gets(inputStr);//如果编译器太古老，改为gets(inputStr)
	int state = run(firstState, inputStr);
	if (state == -1) printf("%s单词有非法符号！\n", inputStr);
	else if (isInEndState(state)) {
		printf("%s单词符合规则，有连续2个a或连续2个b！\n", inputStr);
	}
	else {
		printf("%s单词不符合规则，没有连续a，也没有连续b！\n", inputStr);
	}
	return 0;
}
