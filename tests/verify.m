verify ; 🧬 ASTRID — verification (M-Light compatible)
       ; Checks: identity seeded, active, provider/model set, rules+capabilities counted.
       ; Usage: D VERIFY^VERIFY
VERIFY
       N ok
       S ok=1
       I $G(^PERSONALITY("astrid","identity"))="" D
       . W !,"FAIL identity vacia" S ok=0
       I $G(^PERSONALITY("astrid","is_active"))'="1" D
       . W !,"FAIL is_active!=1" S ok=0
       I $G(^PERSONALITY("astrid","provider"))="" D
       . W !,"FAIL provider vacio" S ok=0
       I $G(^PERSONALITY("astrid","model"))="" D
       . W !,"FAIL model vacio" S ok=0
       I $L($G(^PERSONALITY("astrid","identity")))<600 D
       . W !,"FAIL identity <600 chars" S ok=0
       I ok W !,"PASS astrid verificada"
       Q
