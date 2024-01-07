#include<stdio.h>
#include<stdlib.h>

typedef struct PolyTerm {
    float coef;
    int expn;
    struct PolyTerm* next;
}PolyTerm;

typedef struct Polynomial {
    PolyTerm* head;
}Polynomial;

PolyTerm* new_poly_term(float coef, int expn) {
    PolyTerm* term = (PolyTerm*)malloc(sizeof(PolyTerm));
    term->coef = coef;
    term->expn = expn;
    term->next = NULL;
    return term;
}

Polynomial* new_polynomial() {
    Polynomial* poly = (Polynomial*)malloc(sizeof(Polynomial));
    poly->head = NULL;
    return poly;
}

void add_poly_term(Polynomial* poly, float coef, int expn) {
    PolyTerm* term = new_poly_term(coef, expn);
    if (poly->head == NULL || term->expn < poly->head->expn) {
        term->next = poly->head;
        poly->head = term;
    } else {
        PolyTerm* current = poly->head;
        while (current->next != NULL && current->next->expn > term->expn) {
            current = current->next;
        }
        if (current->expn == term->expn) { // 如果找到相同指数项，则合并系数
            current->coef += term->coef;
            free(term);
        } else {
            term->next = current->next;
            current->next = term;
        }
    }
}

// 合并两个多项式链表，并按指数排序，并处理相同指数项的系数相加
Polynomial* add_two_poly_terms(Polynomial* poly_1, Polynomial* poly_2) {
    if (poly_1->head == NULL) {
        return poly_2;
    }
    if (poly_2->head == NULL) {
        return poly_1;
    }

    Polynomial* tail = new_polynomial();
    PolyTerm* p1 = poly_1->head;
    PolyTerm* p2 = poly_2->head;
    
    while (p1 != NULL && p2 != NULL) {
        if (p1->expn < p2->expn) {
            add_poly_term(tail, p1->coef, p1->expn);
            p1 = p1->next;
        } else if (p1->expn > p2->expn) {
            add_poly_term(tail, p2->coef, p2->expn);
            p2 = p2->next;
        } else { // 索引相同，合并系数并将较小链表的指针指向下一个元素
            add_poly_term(tail, p1->coef + p2->coef, p1->expn);
            p1 = p1->next;
            p2 = p2->next;
        }
    }

    // 将剩余未处理完的链表加入到结果链表中
    while (p1 != NULL) {
        add_poly_term(tail, p1->coef, p1->expn);
        p1 = p1->next;
    }
    while (p2 != NULL) {
        add_poly_term(tail, p2->coef, p2->expn);
        p2 = p2->next;
    }
    Polynomial* sum = new_polynomial();
    PolyTerm* p_tail = tail->head;
    while(p_tail->next && p_tail){
        if(p_tail->next->expn==p_tail->expn){
            p_tail->next->coef=p_tail->next->coef+p_tail->coef;
            add_poly_term(sum, p_tail->next->coef, p_tail->next->expn);
            p_tail=p_tail->next->next;
            if(p_tail==NULL){
                break;
            }
        }
        else{
            add_poly_term(sum, p_tail->coef, p_tail->expn);
            p_tail = p_tail->next;
            if(p_tail==NULL){
                break;
        }
    }
    return sum;
}

int main(void) {
	Polynomial* poly_1 = new_polynomial();
	Polynomial* poly_2 = new_polynomial();
	float coef;
	int expn;
	int i;


	printf("poly_1:\n");
	for (i = 0; i < 5; i++) {
		printf("coef,expn:\n");
		scanf("%f %d", &coef, &expn);
		add_poly_term(poly_1, coef, expn);
	}

	printf("poly_2:\n");
	for (i = 0; i < 5; i++) {
		printf("coef,expn:\n");
		scanf("%f %d", &coef, &expn);
		add_poly_term(poly_2, coef, expn);
	}
	PolyTerm* p1 = poly_1->head;
	PolyTerm* p2 = poly_2->head;

	printf("poly_1:\n");
	for (i = 0; i < 5; i++) {
		printf("%f*X^%d+", p1->coef,p1->expn);
		p1 = p1->next;
	}


	printf("\n");

	printf("poly_2:\n"); 
	for (i = 0; i < 5; i++) {
		printf("%f*X^%d+", p2->coef, p2->expn);
		p2 = p2->next;
	}
	printf("\n");



 // 使用新的 add_two_poly_terms 函数计算和多项式
    Polynomial* poly_add = add_two_poly_terms(poly_1, poly_2);
	PolyTerm* poly = poly_add->head;
	printf("poly=:\n");
	while (poly != NULL) {
		printf("%f*X^%d\n", poly->coef, poly->expn);
		poly = poly->next;
	}
	return 0;
}