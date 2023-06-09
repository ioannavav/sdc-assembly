.section .text
.global print_registers

print_registers:
    sub $2048, %rsp  # Reserve space for ZMM registers

    # Save ZMM registers
    vmovdqu64 %zmm0, 0(%rsp)
    vmovdqu64 %zmm1, 64(%rsp)
    vmovdqu64 %zmm2, 128(%rsp)
    vmovdqu64 %zmm3, 192(%rsp)
    vmovdqu64 %zmm4, 256(%rsp)
    vmovdqu64 %zmm5, 320(%rsp)
    vmovdqu64 %zmm6, 384(%rsp)
    vmovdqu64 %zmm7, 448(%rsp)
    vmovdqu64 %zmm8, 512(%rsp)
    vmovdqu64 %zmm9, 576(%rsp)
    vmovdqu64 %zmm10, 640(%rsp)
    vmovdqu64 %zmm11, 704(%rsp)
    vmovdqu64 %zmm12, 768(%rsp)
    vmovdqu64 %zmm13, 832(%rsp)
    vmovdqu64 %zmm14, 896(%rsp)
    vmovdqu64 %zmm15, 960(%rsp)
    vmovdqu64 %zmm16, 1024(%rsp)
    vmovdqu64 %zmm17, 1088(%rsp)
    vmovdqu64 %zmm18, 1152(%rsp)
    vmovdqu64 %zmm19, 1216(%rsp)
    vmovdqu64 %zmm20, 1280(%rsp)
    vmovdqu64 %zmm21, 1344(%rsp)
    vmovdqu64 %zmm22, 1408(%rsp)
    vmovdqu64 %zmm23, 1472(%rsp)
    vmovdqu64 %zmm24, 1536(%rsp)
    vmovdqu64 %zmm25, 1600(%rsp)
    vmovdqu64 %zmm26, 1664(%rsp)
    vmovdqu64 %zmm27, 1728(%rsp)
    vmovdqu64 %zmm28, 1792(%rsp)
    vmovdqu64 %zmm29, 1856(%rsp)
    vmovdqu64 %zmm30, 1920(%rsp)
    vmovdqu64 %zmm31, 1984(%rsp)


    # push general purpose registers to the stack
    push %rax
    push %rbx
    push %rcx
    push %rdx
    push %rsi
    push %rdi
    push %rbp
    push %r8
    push %r9
    push %r10
    push %r11
    push %r12
    push %r13
    push %r14
    push %r15

    mov 2168(%rsp), %r8  # 2176 is the new offset of the return address from the top of the stack after pushing all these registers and reserving space for ZMM registers
    # push return address to the stack
    push %r8

    # syscall number for write
    mov $1, %rax
    # file descriptor 1 is stdout
    mov $1, %rdi
    # buffer is the address at the top of the stack
    mov %rsp, %rsi

    # length is 8 bytes (64 bits) for each gpr and 2048 bytes for ZMM registers
    mov $2176, %rdx

    # perform the syscall
    syscall

    # pop return address from the stack
    pop %r8

    # pop general purpose registers from the stack
    pop %r15
    pop %r14
    pop %r13
    pop %r12
    pop %r11
    pop %r10
    pop %r9
    pop %r8
    pop %rbp
    pop %rdi
    pop %rsi
    pop %rdx
    pop %rcx
    pop %rbx
    pop %rax

    # Restore ZMM registers
    vmovdqu64 0(%rsp), %zmm0
    vmovdqu64 64(%rsp), %zmm1
    vmovdqu64 128(%rsp), %zmm2
    vmovdqu64 192(%rsp), %zmm3
    vmovdqu64 256(%rsp), %zmm4
    vmovdqu64 320(%rsp), %zmm5
    vmovdqu64 384(%rsp), %zmm6
    vmovdqu64 448(%rsp), %zmm7
    vmovdqu64 512(%rsp), %zmm8
    vmovdqu64 576(%rsp), %zmm9
    vmovdqu64 640(%rsp), %zmm10
    vmovdqu64 704(%rsp), %zmm11
    vmovdqu64 768(%rsp), %zmm12
    vmovdqu64 832(%rsp), %zmm13
    vmovdqu64 896(%rsp), %zmm14
    vmovdqu64 960(%rsp), %zmm15
    vmovdqu64 1024(%rsp), %zmm16
    vmovdqu64 1088(%rsp), %zmm17
    vmovdqu64 1152(%rsp), %zmm18
    vmovdqu64 1216(%rsp), %zmm19
    vmovdqu64 1280(%rsp), %zmm20
    vmovdqu64 1344(%rsp), %zmm21
    vmovdqu64 1408(%rsp), %zmm22
    vmovdqu64 1472(%rsp), %zmm23
    vmovdqu64 1536(%rsp), %zmm24
    vmovdqu64 1600(%rsp), %zmm25
    vmovdqu64 1664(%rsp), %zmm26
    vmovdqu64 1728(%rsp), %zmm27
    vmovdqu64 1792(%rsp), %zmm28
    vmovdqu64 1856(%rsp), %zmm29
    vmovdqu64 1920(%rsp), %zmm30
    vmovdqu64 1984(%rsp), %zmm31

    add $2048, %rsp  # Release stack space for ZMM registers  2032

    ret