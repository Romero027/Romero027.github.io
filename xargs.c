#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/param.h"

int main(int argc, char *argv[]) {

    if (argc < 2) {
        fprintf(2, "usage: xargs command\n");
        exit(1);
    }

    char *_argv[MAXARG]; // command after exec
    for (int i = 1; i < argc; i++) 
        _argv[i - 1] = argv[i];
    char buf[1024];
    char c;
    int stat = 1;

    while(stat) {
        int cnt = 0;
        int argv_cnt = argc - 1;
        int argv_begin = 0;
        while(1) {
            stat = read(0, &c, 1);
            if (!stat)
                exit(0);

            if (c == ' ' || c == '\n') {
                buf[cnt++] = '\0';
                _argv[argv_cnt++] = &buf[argv_begin];
                argv_begin = cnt;
                if (c == '\n') 
                    break
            } else {
                buf[cnt++] = c;
            }
        }
    }

    _argv[argv_cnt] = 0;
    if (fork() == 0)
    {
        exec(_argv[0], _argv);
    }
    else
    {
        wait(0);
    }
}