#include <stdint.h>

typedef union {
    struct {
        int32_t a:4;
        int32_t b:12;
    } s;
    uint16_t v;
} my_s;
void doit(
        my_s * s);

void doit(my_s * s) {
	uintptr_t ptr = (uintptr_t)&s->s;
//    printf("Hello");
}

