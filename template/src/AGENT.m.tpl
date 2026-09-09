__NAME__ ; __EMOJI__ __NAME__ — derived from the Astrid template (MIT)
         ; Template: https://github.com/GonzaloMonzonC/astrid (template/)
         ; Contract mirrors src/astrid.m — see docs/DESIGN.md "Interfaz con lumen".
         ;   D __NAMEU__^__NAMEU__     status
         ;   D INIT^__NAMEU__          seed ^PERSONALITY("__NAME__") — fill missing
         ;   D INIT^__NAMEU__(1)       seed and overwrite (force)

__NAMEU__ ; ---- status ----
         N ident,act
         S ident=$G(^PERSONALITY("__NAME__","identity"))
         S act=$G(^PERSONALITY("__NAME__","is_active"))
         W !,"__EMOJI__ __NAME__ v",$G(^PERSONALITY("__NAME__","version"))," | active=",act
         W !,"identity_len=",$L(ident)
         W !,"provider=",$G(^PERSONALITY("__NAME__","provider"))," model=",$G(^PERSONALITY("__NAME__","model"))
         Q

INIT(force) ; seed ^PERSONALITY("__NAME__") — fill missing unless force=1
         I $G(force)=1 K ^PERSONALITY("__NAME__")
         D SEED^__NAMEU__
         W !,"INIT: semilla de __NAME__ lista (v",$G(^PERSONALITY("__NAME__","version")),")"
         Q

SEED ; canonical seed (SETIF only writes missing)
         D SETIF^__NAMEU__("name","__NAME__")
         D SETIF^__NAMEU__("role","__ROLE__")
         D SETIF^__NAMEU__("identity","__IDENTITY__")
         D SETIF^__NAMEU__("category","__CATEGORY__")
         D SETIF^__NAMEU__("emoji","__EMOJI__")
         D SETIF^__NAMEU__("color","__COLOR__")
         D SETIF^__NAMEU__("core_mission","__CORE_MISSION__")
         D SETIF^__NAMEU__("status","registrado")
         D SETIF^__NAMEU__("is_active","1")
         D SETIF^__NAMEU__("provider","deepseek")
         D SETIF^__NAMEU__("model","deepseek-v4-flash")
         D SETIF^__NAMEU__("temperature","0.3")
         D SETIF^__NAMEU__("creator","astrid-template")
         D SETIF^__NAMEU__("version","0.1.0")
         D RULES^__NAMEU__
         D CAPS^__NAMEU__
         D PEERS^__NAMEU__
         Q

SETIF(field,val) ; write only if missing
         I $G(^PERSONALITY("__NAME__",field))="" S ^PERSONALITY("__NAME__",field)=val
         Q

RULES ; write rules only if the list is missing
         N k
         S k=$O(^PERSONALITY("__NAME__","critical_rules",""))
         I k="" D
         . S ^PERSONALITY("__NAME__","critical_rules","1")="__RULE_1__"
         . S ^PERSONALITY("__NAME__","critical_rules","2")="__RULE_2__"
         . S ^PERSONALITY("__NAME__","critical_rules","3")="__RULE_3__"
         Q

CAPS ; capabilities only if missing
         N k
         S k=$O(^PERSONALITY("__NAME__","capabilities",""))
         I k="" D
         . S ^PERSONALITY("__NAME__","capabilities","__CAP_1__")="__CAP_1_DESC__"
         . S ^PERSONALITY("__NAME__","capabilities","__CAP_2__")="__CAP_2_DESC__"
         Q

PEERS ; peers only if missing
         N k
         S k=$O(^PERSONALITY("__NAME__","peers",""))
         I k="" D
         . S ^PERSONALITY("__NAME__","peers","astrid")="template/reference agent"
         . S ^PERSONALITY("__NAME__","peers","poli")="mother runtime"
         . S ^PERSONALITY("__NAME__","peers","smith")="multi-personality orchestrator"
         Q
