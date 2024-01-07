#include<iostream>
#include <random>
#include <ctime>
#include <string>
#include <fstream>
#define    Normal int
#define    WeightChecking char


template<typename T>
class my_vector {
private:
    class Node {
    public:
        T node_data;
        Node* next;
    };
    Node* head;
    Node* tail;

    int node_size;

public:
    // 添加构造函数
    my_vector() : node_size(0), head(nullptr), tail(nullptr) {}
    void push_back(T t) {
        Node* new_node = new Node;
        new_node->node_data = t;
        new_node->next = nullptr;

        if (head == nullptr) {
            head = new_node;
            tail = new_node;
        }
        else {
            tail->next = new_node;
            tail = new_node;
        }
        ++node_size;
    }
    
    T& operator[](int index) {
        Node* p = head;
        try{
        if (!p) {
            throw "error";
        }
        }catch(char *s){
            printf("error");
        }

        for (int i = 0; i < index; i++) {
            p = p->next;
        }

        return p->node_data;
    }

    int my_size() { return node_size; }


};

class Vehicle {
public:
    // 构造函数，初始化车辆的基本信息
    virtual ~Vehicle() {}

    Vehicle(int licensePlate, std::string VIN, char Id, int waitingTime)
        : licensePlate(licensePlate), VIN(VIN), time_of_head_to_channel(-1), all_waiting_time(0), is_in_channel(false), car_id(Id), init_waiting_time(waitingTime), visited(false), is_waiting(false), if_is_constant(false) {}

    // 获取车牌号的getter方法
    int getLicensePlate() const { return licensePlate; }
    // 获取VIN的getter方法
    std::string getVIN() const { return VIN; }

    //设置进入通道的时间
    void set_time_to_channer(int time) { time_of_head_to_channel = time; }

    void add_waiting_time() { all_waiting_time++; }

    void set_is_in_channel(bool i) { is_in_channel = i; }

    bool get_is_in_channel() const { return is_in_channel; }

    int get_time_to_channer() const { return time_of_head_to_channel; }

    void set_in_which_channel(int i) { in_which_channel = i; }

    int get_in_which_channel() const { return in_which_channel; }

    char get_car_id() const { return car_id; }

    void set_init_waiting_time(int i) { init_waiting_time = i; }

    int get_init_waiting_time() { return init_waiting_time; }

    int get_all_waiting_time() { return all_waiting_time; }

    bool getVisited() { return visited; }

    void setVisited(bool is) { visited = is; }

    void set_iswaiting(bool is) { is_waiting = is; }

    bool get_iswaiting() { return is_waiting; }


    void set_if_is_constant(bool is) { if_is_constant = is; }

    bool get_if_is_constant() { return if_is_constant; }
private:
    int licensePlate;

    std::string VIN;

    //60秒的话，第几秒进入的通道呢~
    int time_of_head_to_channel;

    //需要的等待时间
    int init_waiting_time;

    //已经等待的时间
    int all_waiting_time;

    bool is_in_channel;

    //在哪一个channel
    int in_which_channel;

    char car_id;

    //修复重复的bug
    bool visited;


    bool is_waiting;

    bool if_is_constant;
};


class PassengerCar : public Vehicle {
public:
    // 构造函数，初始化客车的基本信息和座位数
    PassengerCar(int licensePlate, std::string VIN, int seatCount, int waitingTime)
        : Vehicle(licensePlate, VIN, 'c', waitingTime), seatCount(seatCount) {}

    // 获取座位数的getter方法
    int getSeatCount() const { return seatCount; }

private:
    // 座位数
    int seatCount;

};


class CargoCar : public Vehicle {
public:
    // 构造函数，初始化货车的基本信息、载重量、车轴数量和是否为农产品货车
    CargoCar(int licensePlate, std::string VIN, double loadWeight, int axleCount, bool isAgricultural, bool empty, int waitingTime)
        : Vehicle(licensePlate, VIN, 'h', waitingTime), loadWeight(loadWeight), axleCount(axleCount), isAgricultural(isAgricultural), isEmpty(empty) {}

    // 获取载重量的getter方法
    double getLoadWeight() const { return loadWeight; }
    // 获取车轴数量的getter方法
    int getAxleCount() const { return axleCount; }
    // 判断是否为农产品货车的getter方法
    bool getIsAgricultural() { return isAgricultural; }


    bool get_isEmpty() const { return isEmpty; }

    void set_isEmpty(bool value) { isEmpty = value; }
private:
    // 载重量
    double loadWeight;
    // 车轴数量
    int axleCount;
    // 是否为农产品货车
    bool isAgricultural;

    bool isEmpty;
};

class TollChannelBase {
public:
    // 构造函数，初始化收费通道的基本信息
    TollChannelBase(bool is)
        :queueSize(0), isOpen(is) {}

    int getQueueSize() const { return queueSize; }
    //int getWaitingTime() const { return waitingTime; }

    void add_QueueSize() { queueSize += 1; }

    bool getIsOpen() const { return isOpen; }

    void set_waiting_Time(int t) { waitingTime = t; }

    void set_channelId(int i) { channelId = i; }

    int get_channelId() const { return channelId; }

    void drop_QueueSize() { queueSize -= 1; }
protected:
    //是否开放
    bool isOpen;

    // 当前排队车辆数量
    int queueSize;

    // 当前等待时间
    int waitingTime;

    //Id
    int channelId;
};

template <typename T>
class TollChannel :public TollChannelBase {
public:
    TollChannel()
        : TollChannelBase(true) {}
};


// 普通通道模板类
template <>
class TollChannel<Normal> :public TollChannelBase {
public:
    TollChannel()
        : TollChannelBase(true) {}

};

// 称重通道模板类
template <>
class TollChannel<WeightChecking> : public TollChannelBase {
public:
    TollChannel()
        : TollChannelBase(true) {}

};

std::string generateRandomVIN() {
    static const char alphanum[] =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        ;

    std::string VIN;
    for (int i = 0; i < 17; ++i) {
        VIN += alphanum[rand() % sizeof(alphanum)];
    }
    return VIN;
}

int generateRandomCar(my_vector<Vehicle*>& vehicles) {

    int numCars = rand() % 31 + 20;
    int numPassengerCar = numCars * 0.6;
    int numCargoCar = numCars * 0.4;
    int numEmptyCargoCar = numCargoCar * 0.25;
    int numFullCargoCar = numCargoCar * 0.75;
    int numAgricultural = numFullCargoCar * 0.3;
    int numNotAgricultural = numFullCargoCar * 0.7;

    //Passenger vehicle
    for (int i = 0; i < numPassengerCar; i++) {
        int seatCount = rand() % 49 + 2;

        int licensePlate = rand() % 10001 + 10000;

        std::string VIN = generateRandomVIN();

        int waitint_time = rand() % 31 + 30;
        // 创建一个新的PassengerCar对象，并将其添加到vehicles向量中
        vehicles.push_back(new PassengerCar(licensePlate, VIN, seatCount, waitint_time));
    }
    //EmptyCargoCar
    for (int i = 0; i < numEmptyCargoCar; i++) {
        int licensePlate = rand() % 10001 + 10000;

        std::string VIN = generateRandomVIN();

        int waitingTime = rand() % 31 + 30;
        // 创建一个新的CargoCar对象（空载货车），并将其添加到vehicles向量中
        vehicles.push_back(new CargoCar(licensePlate, VIN, 0.0, 2, false, true, waitingTime));


    }
    //Agricultural
    for (int i = 0; i < numAgricultural; i++) {

        bool isAgricultural = true;

        double loadWeight = rand() % 49 + 0.5;

        int axleCount = rand() % 4 + 2;

        int licensePlate = rand() % 10001 + 10000;

        int waitingTime = rand() % 181 + 120;

        std::string VIN = generateRandomVIN();

        // 创建一个新的CargoCar对象（载重货车），并将其添加到vehicles向量中
        vehicles.push_back(new CargoCar(licensePlate, VIN, loadWeight, axleCount, isAgricultural, false, waitingTime));
    }
    //NotAgricultural
    for (int i = 0; i < numNotAgricultural; i++) {

        bool isAgricultural = false;

        double loadWeight = rand() % 49 + 0.5;
        int axleCount = rand() % 4 + 2;

        int licensePlate = rand() % 10001 + 10000;

        std::string VIN = generateRandomVIN();

        int waitingTime = rand() % 111 + 90;

        // 创建一个新的CargoCar对象（载重货车），并将其添加到vehicles向量中
        vehicles.push_back(new CargoCar(licensePlate, VIN, loadWeight, axleCount, isAgricultural, false, waitingTime));
    }

    return numPassengerCar + numEmptyCargoCar + numAgricultural + numNotAgricultural;
}

bool all_channels_are_full_vehicles(TollChannel<WeightChecking> WeightCheckingchannel, my_vector<TollChannel<Normal>> channels) {
    int num = 0;
    num += WeightCheckingchannel.getQueueSize();
    for (int i = 0; i < channels.my_size(); i++) {
        num += channels[i].getQueueSize();

    }
    if (num >= (1 + channels.my_size()) * 20)
        return true;
    return false;
}

//设置一分钟内进入通道的时间
void set_all_vehicles_time_of_head_to_channel(my_vector<Vehicle*> vehicles) {

    for (int i = 0; i < vehicles.my_size(); i++) {
        if (vehicles[i]->get_iswaiting()) {
            continue;
        }
        else {
            int s = rand() % 60 + 1;
            vehicles[i]->set_time_to_channer(s);
        }

    }
}

//0是特殊通道，其他正常
int get_min_vehicle_channels_Id(TollChannel<WeightChecking> WeightCheckingchannel, my_vector<TollChannel<Normal>> channels) {
    int min_num = WeightCheckingchannel.getQueueSize();
    int min_channelId = 0;
    for (int i = 0; i < channels.my_size(); i++) {
        if (channels[i].getQueueSize() < min_num) {
            min_num = channels[i].getQueueSize();
            min_channelId = i + 1;
        }
    }
    return min_channelId;
}

my_vector<Vehicle*> vehicles;

int main(int argc, char**) {
    // 称重收费通道
    TollChannel<WeightChecking> WeightCheckingchannel;
    my_vector<TollChannel<Normal>> channels;
    channels.push_back(TollChannel<Normal>());
    FILE* f = fopen("read.txt", "w");

    if (!f) {
        std::cerr << "Error: Unable to open the output file 'read.txt'!" << std::endl;
        return 1;
    }
    srand(time(0));

    //60次，每次代表一分钟
    try {
        int cishu = 0;
        for (int up_i = 1; up_i <= 60; up_i++) {
            //每分钟初始化车辆
            generateRandomCar(vehicles);
            set_all_vehicles_time_of_head_to_channel(vehicles);

            //60次，每次代表一秒
            for (int down_i = 1; down_i <= 60; down_i++) {
                cishu++;
                //如果全满了,尝试增加通道
                if (all_channels_are_full_vehicles(WeightCheckingchannel, channels)) {
                    if ((channels.my_size() + 1) > 8)
                        throw "all_channels_are_full_vehicles";
                    else {
                        channels.push_back(TollChannel<Normal>());
                    }
                }
                //当前通道没满的话或者增加过通道了,那么就找到当前最短的通道进入
                //遍历所有车辆
                for (int i = 0; i < vehicles.my_size(); i++) {
                    vehicles[i]->set_iswaiting(true);
                    //如果标记在通道内，每一秒加时间即可
                    //注意：此时当这一次循环结束之后，down的值清0，也就是有些车永远出不去
                    if (!vehicles[i]->getVisited() && vehicles[i]->get_if_is_constant()) {
                        vehicles[i]->add_waiting_time();
                        if (vehicles[i]->get_init_waiting_time() <= vehicles[i]->get_all_waiting_time()) {
                            Vehicle* to_Delete = vehicles[i];

                            int id = vehicles[i]->get_in_which_channel();
                            if (id == 0) {
                                WeightCheckingchannel.drop_QueueSize();
                            }
                            else {
                                channels[id - 1].drop_QueueSize();
                            }
                            vehicles[i]->set_is_in_channel(false);
                            vehicles[i]->setVisited(true);
                            vehicles[i]->set_if_is_constant(false);
                            if (vehicles[i]->get_car_id() == 'c') {
                                PassengerCar* c = (PassengerCar*)vehicles[i];
                                fprintf(f, "客车VIN: %s  车牌:%d  out  \n等待时间： %d秒 \n座位数：%d\n", vehicles[i]->getVIN().c_str(), vehicles[i]->getLicensePlate(), vehicles[i]->get_all_waiting_time(), c->getSeatCount());
                            }
                            else {
                                CargoCar* h = (CargoCar*)vehicles[i];
                                if (h->getIsAgricultural()) {
                                    fprintf(f, "农车VIN: %s  车牌:%d  out  \n等待时间： %d秒 \n载重量：%d \n车轴数量：%d\n走的通道：称重收费通道\n", vehicles[i]->getVIN().c_str(), vehicles[i]->getLicensePlate(), vehicles[i]->get_all_waiting_time(), h->getLoadWeight(), h->getAxleCount());
                                }
                                else {
                                    fprintf(f, "货车VIN: %s  车牌:%d  out  \n等待时间： %d秒 \n载重量：%d \n车轴数量：%d\n", vehicles[i]->getVIN().c_str(), vehicles[i]->getLicensePlate(), vehicles[i]->get_all_waiting_time(), h->getLoadWeight(), h->getAxleCount());
                                }
                            }
                        }
                    }

                    else if (!vehicles[i]->getVisited() && vehicles[i]->get_is_in_channel() && vehicles[i]->get_time_to_channer() <= down_i) {
                        vehicles[i]->add_waiting_time();
                        vehicles[i]->set_if_is_constant(true);
                        if (vehicles[i]->get_init_waiting_time() <= vehicles[i]->get_all_waiting_time()) {
                            Vehicle* to_Delete = vehicles[i];

                            int id = vehicles[i]->get_in_which_channel();
                            if (id == 0) {
                                WeightCheckingchannel.drop_QueueSize();
                            }
                            else {
                                channels[id - 1].drop_QueueSize();
                            }
                            vehicles[i]->set_is_in_channel(false);
                            vehicles[i]->setVisited(true);
                        }

                    }
                    //是否时间大于等待时间，那么就出去;
                    //如果不在，并且时间已经到了，那么就要让车进入通道
                    //选择车最少的通道。
                    //判断车的类型！
                    else if (!vehicles[i]->getVisited() && !vehicles[i]->get_is_in_channel() && vehicles[i]->get_time_to_channer() <= down_i) {
                        vehicles[i]->set_is_in_channel(true);
                        vehicles[i]->add_waiting_time();
                        int channel_id = get_min_vehicle_channels_Id(WeightCheckingchannel, channels);
                        //客车
                        if (vehicles[i]->get_car_id() == 'c') {
                            vehicles[i]->set_in_which_channel(channel_id);
                            if (channel_id == 0) {
                                WeightCheckingchannel.add_QueueSize();
                            }
                            else if (channel_id != 0) {
                                channels[channel_id - 1].add_QueueSize();
                            }
                        }
                        //货车
                        else if (vehicles[i]->get_car_id() == 'h') {
                            CargoCar* Car_p = (CargoCar*)vehicles[i];
                            if (!Car_p->get_isEmpty()) {
                                WeightCheckingchannel.add_QueueSize();
                                vehicles[i]->set_in_which_channel(0);
                            }
                            else {
                                WeightCheckingchannel.add_QueueSize();
                                vehicles[i]->set_in_which_channel(channel_id);
                            }
                        }

                    }

                }

            }

        }

    }
    catch (const char* errMsg) {
        std::cerr << "Error: " << errMsg << std::endl;
    }

    fclose(f);
    // 程序正常结束，返回0
    return 0;
}