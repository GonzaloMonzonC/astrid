VERIFY(name) ; 🧬 verification for any ^PERSONALITY agent (M-Light compatible)
        ; Checks: identity seeded (>=600 chars), active, provider/model set.
        ; Usage: D VERIFY^VERIFY            -> checks "astrid"
        ;        D VERIFY^VERIFY("echo")    -> checks any other agent
        N ok,nm
        S nm=$G(name,"astrid")
        S ok=1
        I $G(^PERSONALITY(nm,"identity"))="" D
        . W !,"FAIL identity vacia para ",nm S ok=0
        I $G(^PERSONALITY(nm,"is_active"))'="1" D
        . W !,"FAIL is_active!=1 para ",nm S ok=0
        I $G(^PERSONALITY(nm,"provider"))="" D
        . W !,"FAIL provider vacio para ",nm S ok=0
        I $G(^PERSONALITY(nm,"model"))="" D
        . W !,"FAIL model vacio para ",nm S ok=0
        I $L($G(^PERSONALITY(nm,"identity")))<600 D
        . W !,"FAIL identity <600 chars para ",nm S ok=0
        I ok W !,"PASS ",nm," verificado"
        Q
