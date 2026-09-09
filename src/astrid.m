astrid ; 🧬 ASTRID — reference agent for LUMEN (MIT)
       ; First native of Poli with open code. Identity lives in ^PERSONALITY("astrid").
       ; Depends on lumen-protocol (PDB, MVM, M-Light, Poli+Smith).
       ; Entry points:
       ;   D ASTRID^ASTRID     status: identity + capabilities + rules count
       ;   D INIT^ASTRID       seed ^PERSONALITY("astrid") fields if missing
       ;   D AUDIT^ASTRID      demo audit: count nodes under a namespace
       ;
       ; MIT — see LICENSE. No ecosystem-private lore here: this file is the
       ; public skeleton that any agent can fork.

ASTRID ; status
       N ident,act
       S ident=$G(^PERSONALITY("astrid","identity"))
       S act=$G(^PERSONALITY("astrid","is_active"))
       W !,"🧬 Astrid v",$G(^PERSONALITY("astrid","version"))," | active=",act
       W !,"identity_len=",$L(ident)
       W !,"capabilities=",$$COUNT^ASTRID("capabilities")," rules=",$$COUNT^ASTRID("critical_rules")
       W !,"provider=",$G(^PERSONALITY("astrid","provider"))," model=",$G(^PERSONALITY("astrid","model"))
       Q

INIT ; seed personality fields (idempotent: only fills missing)
       N f
       ; Minimal canonical seed — full identity text lives in personalities/astrid.md
       F f="name","role","identity","category","emoji","color","core_mission","communication_style","status","is_active","provider","model" D
       . I $G(^PERSONALITY("astrid",f))="" S ^PERSONALITY("astrid",f)="PENDING_SEED"  ; replaced by harvester
       W !,"INIT: identity fields ready. Run D ASTRID^ASTRID to verify."
       Q

COUNT(ns) ; count subnodes under ^PERSONALITY("astrid",ns,*) — M-Light compatible
       N k,n
       S n=0
       S k=$O(^PERSONALITY("astrid",ns,""))
       I k="" Q 0
       F  Q:k=""  D
       . S n=n+1
       . S k=$O(^PERSONALITY("astrid",ns,k))
       Q n

AUDIT ; demo: audit a namespace node count (observacion -> implicacion -> pregunta)
       ; usage: D AUDIT^ASTRID^ASTRID("^ANGI")  or  D AUDIT^ASTRID with default
       N ns,k,n
       S ns=$G(^ASTRID("audit_ns"),"^ANGI")
       S n=0
       S k=$O(@ns@(""))
       F  Q:k=""  D
       . S n=n+1
       . S k=$O(@ns@(k))
       W !,"[ASTRID] observacion: ",ns," tiene ",n," entradas de primer nivel"
       W !,"[ASTRID] implicacion: si n=0 o n crece sin control, algo no cuadra con el estado esperado"
       W !,"[ASTRID] pregunta: ^",$P(ns,"^",2)," deberia tener entradas? (confirma con el operador antes de actuar)"
       Q
