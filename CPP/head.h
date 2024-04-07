#include<iostream>
#include<string>
#include<stack>

class Complex {
public:
    // 构造函数
    Complex(double real = 0.0, double imag = 0.0) : real_(real), imaginary_(imag) {}

    // 成员函数
    double get_real() const {return real_;}
    double get_imaginary() const {return imaginary_;}
    void set_real(double real) {real_ = real;}
    void set_imaginary(double imag) {imaginary_ = imag;}
    Complex operator+(const Complex& other) {
        return Complex(this->get_real() + other.get_real(), this->get_imaginary() + other.get_imaginary());
    };

private:
    double real_;
    double imaginary_;
};

class Clock {
public:
    // 构造函数
    Clock(int hour = 0, int minute = 0, int second = 0) : hour_(hour), minute_(minute), second_(second) {}

    int get_hour() const {return hour_;}
    int get_minute() const {return minute_;}
    int get_second() const {return second_;}
    void add_second() {second_++; if (second_ == 60) {add_minute(); second_ = 0;}}
    void add_hour() {hour_++; if (hour_ == 24) {hour_ = 0;}}
    void add_minute() {minute_++;}

private:
    int hour_;
    int minute_;
    int second_;
};

class Book {
public:
    // 构造函数
    Book(const std::string& title, const std::string& author, int publicationYear)
        : title_(title), author_(author), publicationYear_(publicationYear) {}

    // 成员函数
    std::string get_title() const {return title_;}
    std::string get_author() const {return author_;}
    int get_publicationYear() const {return publicationYear_;}
    void set_title(const std::string& title) {title_ = title;}
    void set_author(const std::string& author) {author_ = author;}
    void set_publicationYear(int year) {publicationYear_ = year;}

private:
    std::string title_;
    std::string author_;
    int publicationYear_;
};

class Date {
public:
    // 构造函数
    Date(int year, int month, int day) : year_(year), month_(month), day_(day) {}

    // 成员函数
    int get_year() const {return year_;}
    int get_month() const {return month_;}
    int get_day() const {return day_;}
    void set_year(int year) {year_ = year;}
    void set_month(int month) {month_ = month;}
    void set_day(int day) {day_ = day;}

private:
    int year_;
    int month_;
    int day_;
};

template <typename T>
class Stack {
public:
    // 构造函数
    Stack() {}

    // 成员函数
    bool is_empty() const {return stack_.empty();}
    void push(const T& item) {stack_.push(item);}
    void pop() {if (!is_empty()) stack_.pop();}
    T top() const {if (!is_empty()) return stack_.top(); else throw std::out_of_range("Stack is empty!");}

private:
    std::stack<T> stack_; 
};