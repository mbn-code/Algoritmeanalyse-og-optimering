#ifndef APP_H
#define APP_H

class App {
    private: 
        int version = 1;
    
    public:
        App();
        ~App();
        void run();

        static void run (int argc, char* argv[]);
};

#endif // APP_H