// Validate a built runtime using the same handoff contract as LUNA itself.
#include "luna_psxcore.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s runtime.elf\n", argv[0]);
        return 2;
    }
    FILE *file = fopen(argv[1], "rb");
    if (!file) { perror(argv[1]); return 1; }
    void *bytes = malloc(LUNA_PSX_CAPACITY + 1U);
    if (!bytes) { fclose(file); return 1; }
    const size_t size = fread(bytes, 1, LUNA_PSX_CAPACITY + 1U, file);
    const int read_error = ferror(file);
    const int close_error = fclose(file);
    NpElf elf;
    const char *error = read_error || close_error ? "runtime-read" :
        lunaPsxBootstrapCheck(bytes, size, &elf);
    free(bytes);
    if (error) { fprintf(stderr, "PSXCore runtime rejected: %s\n", error); return 1; }
    printf("PSXCore runtime accepted: entry=%08x segments=%u bytes=%zu\n",
           elf.entry, elf.count, size);
    return 0;
}
