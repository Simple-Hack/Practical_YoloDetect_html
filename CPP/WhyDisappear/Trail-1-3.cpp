%{ 
    #define PROGRAM 1
    #define IDNAME 58
    #define VARSYM 2
    #define SEMICOLONSYM 47
    #define COLONSYM 41
    #define INTEGER 3
    #define BEGINSYM 8
    #define ASSIGNSYM 39
    #define NUMSYM 53
    #define PLUSSYM 30
    #define ENDSYM 26
    #define DOTSYM 50
    #define CHARSYM 6
 
 
    int linenum = 1;
    int errornum = 0;
%} 
 
Digit0 [1-9]
Digit [0-9]
Letter [a-zA-Z]
Integer {Digit}+
Id {Letter | _}({Letter}|{Digit}|_)*
delim [ \t] 
newline [\n]
whitespace {delim}+ 
Real ({Integer}[.]{Integer})([Ee][+-]?{Integer})? 
 
 
invalId {Digit}({Letter}|{Digit}|_)*
invalLetter [^(Letter)(Digit)-*/\+|_'"!]
%% 
[pP][rR][oO][gG][rR][aA][mM]            { printf("%-5d %10s %6d\n",linenum, yytext, PROGRAM);}
[Bb][Ee][Gg][Ii][Nn]                    { printf("%-5d %10s %6d\n",linenum, yytext, BEGINSYM);}
[eE][nN][dD]                            { printf("%-5d %10s %6d\n",linenum, yytext, ENDSYM);}
[iI][nN][tT][eE][gG][eE][rR]            { printf("%-5d %10s %6d\n",linenum, yytext, INTEGER);}
[vV][aA][rR]                            { printf("%-5d %10s %6d\n",linenum, yytext, VARSYM);}
[cC][hH][aA][rR]                        { printf("%-5d %10s %6d\n",linenum, yytext, CHARSYM);}                     
{newline}               { linenum++;}
{whitespace}            { /* do nothing*/ } 
"."                     { printf("%-5d %10s %6d\n",linenum, yytext, DOTSYM);}
";"                     { printf("%-5d %10s %6d\n",linenum, yytext, SEMICOLONSYM);}
":"                     { printf("%-5d %10s %6d\n",linenum, yytext, COLONSYM);}
":="                    { printf("%-5d %10s %6d\n",linenum, yytext, ASSIGNSYM);}
"+"                     { printf("%-5d %10s %6d\n",linenum, yytext, PLUSSYM);}
{Id}                    { printf("%-5d %10s %6d\n",linenum, yytext, IDNAME);}
{Integer}|{Real}        { printf("%-5d %10s %6d\n",linenum, yytext, NUMSYM);}
{invalLetter}           { errornum++; printf("[ERROR]:line %d: 无法识别的字符：%s\n", linenum, yytext);}
{invalId}               { errornum++; printf("[ERROR]:line %d: 无法识别的标识符： %s\n", linenum, yytext);}
%% 
void main() 
{ 
    printf("token表信息：\n"); 
    printf("%-10s %10s %10s\n","行号","名称","种别码"); 
    yylex();
    
    printf("\n词法分析错误信息：\n"); 
    printf("%d error(s)\n", errornum); 
} 
int yywrap() 
{ 
    return 1; 
}
