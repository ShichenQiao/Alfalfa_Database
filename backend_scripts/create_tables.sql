CREATE TABLE "ID_to_uniqueid" (
	"ID"	TEXT NOT NULL UNIQUE,
	"start"	INTEGER NOT NULL UNIQUE,
	"end"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("start","ID","end")
);

CREATE TABLE "alltpm" (
	"GeneID"	TEXT NOT NULL UNIQUE,
	"150_trueleaf_rep1"	REAL NOT NULL,
	"150_xia_rep1"	REAL NOT NULL,
	"150_ziye_rep1"	REAL NOT NULL,
	"fennie_rep1"	REAL NOT NULL,
	"flower_bud_rep1"	REAL NOT NULL,
	"flower_rep1"	REAL NOT NULL,
	"flower_rep2"	REAL NOT NULL,
	"flower_rep3"	REAL NOT NULL,
	"flower_rep4"	REAL NOT NULL,
	"flower_rep5"	REAL NOT NULL,
	"flower_rep6"	REAL NOT NULL,
	"flower_rep7"	REAL NOT NULL,
	"flower_rep8"	REAL NOT NULL,
	"germ_seed_rep1"	REAL NOT NULL,
	"guojia_rep1"	REAL NOT NULL,
	"lateral_root_rep1"	REAL NOT NULL,
	"leaf_bud_rep1"	REAL NOT NULL,
	"leaf_bud_rep2"	REAL NOT NULL,
	"leaf_bud_rep3"	REAL NOT NULL,
	"main_root_rep1"	REAL NOT NULL,
	"mature_leaf_rep1"	REAL NOT NULL,
	"mature_leaf_rep2"	REAL NOT NULL,
	"mature_leaf_rep3"	REAL NOT NULL,
	"MS_trueleaf_rep1"	REAL NOT NULL,
	"MS_xia_rep1"	REAL NOT NULL,
	"MS_ziye_rep1"	REAL NOT NULL,
	"nod_21_rep1"	REAL NOT NULL,
	"nod_28_rep1"	REAL NOT NULL,
	"seed_rep1"	REAL NOT NULL,
	"stem_branch_rep1"	REAL NOT NULL,
	"stem_rep1"	REAL NOT NULL,
	"yige_rep1"	REAL NOT NULL,
	"yige_rep2"	REAL NOT NULL,
	"yige_rep3"	REAL NOT NULL,
	"young_leaf_rep1"	REAL NOT NULL,
	"young_leaf_rep2"	REAL NOT NULL,
	"young_leaf_rep3"	REAL NOT NULL,
	PRIMARY KEY("GeneID")
);

CREATE TABLE "annotate_info" (
	"ID_full"	TEXT NOT NULL,
	"db_name"	TEXT NOT NULL,
	"info1"	TEXT,
	"info2"	TEXT,
	CONSTRAINT "FK_annotate" FOREIGN KEY("ID_full") REFERENCES "pros_info"("ID_full")
);

CREATE TABLE "gff" (
	"unique_id"	INTEGER NOT NULL UNIQUE,
	"seqid"	TEXT NOT NULL,
	"source"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"start"	INTEGER NOT NULL,
	"end"	INTEGER NOT NULL,
	"score"	TEXT NOT NULL,
	"strand"	TEXT NOT NULL,
	"phase"	TEXT NOT NULL,
	"attributes"	TEXT NOT NULL,
	"DNA"	TEXT NOT NULL,
	PRIMARY KEY("unique_id" AUTOINCREMENT)
);

CREATE TABLE "go_info" (
	"ID_full"	TEXT NOT NULL UNIQUE,
	"go"	TEXT NOT NULL,
	PRIMARY KEY("ID_full"),
	CONSTRAINT "FK_go" FOREIGN KEY("ID_full") REFERENCES "pros_info"("ID_full")
);

CREATE TABLE "interpro_info" (
	"ID_full"	TEXT NOT NULL UNIQUE,
	"interpro"	TEXT NOT NULL,
	PRIMARY KEY("ID_full"),
	CONSTRAINT "FK_interpro" FOREIGN KEY("ID_full") REFERENCES "pros_info"("ID_full")
);

CREATE TABLE "kegg_info" (
	"ID_full"	TEXT NOT NULL UNIQUE,
	"kegg"	TEXT NOT NULL,
	PRIMARY KEY("ID_full"),
	CONSTRAINT "FK_kegg" FOREIGN KEY("ID_full") REFERENCES "pros_info"("ID_full")
);

CREATE TABLE "pathway_info" (
	"ID_full"	TEXT NOT NULL UNIQUE,
	"pathway"	TEXT NOT NULL,
	PRIMARY KEY("ID_full"),
	CONSTRAINT "FK_pathway" FOREIGN KEY("ID_full") REFERENCES "pros_info"("ID_full")
);

CREATE TABLE "pfam_info" (
	"ID_full"	TEXT NOT NULL UNIQUE,
	"pfam"	TEXT NOT NULL,
	PRIMARY KEY("ID_full"),
	CONSTRAINT "FK_pfam" FOREIGN KEY("ID_full") REFERENCES "pros_info"("ID_full")
);

CREATE TABLE "pros_info" (
	"unique_id"	INTEGER NOT NULL UNIQUE,
	"ID_full"	TEXT NOT NULL UNIQUE,
	"pros"	TEXT NOT NULL,
	CONSTRAINT "FK" FOREIGN KEY("unique_id") REFERENCES "gff"("unique_id"),
	PRIMARY KEY("unique_id","ID_full")
);

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE "vcf" (
	"vcf_ID"	INTEGER NOT NULL UNIQUE,
	"CHROM"	TEXT NOT NULL,
	"POS"	INTEGER NOT NULL,
	"REF"	TEXT NOT NULL,
	"ALT"	TEXT NOT NULL,
	"C1"	TEXT NOT NULL,
	"C10"	TEXT NOT NULL,
	"C100"	TEXT NOT NULL,
	"C101"	TEXT NOT NULL,
	"C102"	TEXT NOT NULL,
	"C103"	TEXT NOT NULL,
	"C104"	TEXT NOT NULL,
	"C105"	TEXT NOT NULL,
	"C106"	TEXT NOT NULL,
	"C107"	TEXT NOT NULL,
	"C108"	TEXT NOT NULL,
	"C109"	TEXT NOT NULL,
	"C11"	TEXT NOT NULL,
	"C110"	TEXT NOT NULL,
	"C111"	TEXT NOT NULL,
	"C112"	TEXT NOT NULL,
	"C113"	TEXT NOT NULL,
	"C114"	TEXT NOT NULL,
	"C115"	TEXT NOT NULL,
	"C116"	TEXT NOT NULL,
	"C117"	TEXT NOT NULL,
	"C118"	TEXT NOT NULL,
	"C119"	TEXT NOT NULL,
	"C12"	TEXT NOT NULL,
	"C120"	TEXT NOT NULL,
	"C121"	TEXT NOT NULL,
	"C122"	TEXT NOT NULL,
	"C123"	TEXT NOT NULL,
	"C124"	TEXT NOT NULL,
	"C125"	TEXT NOT NULL,
	"C126"	TEXT NOT NULL,
	"C127"	TEXT NOT NULL,
	"C128"	TEXT NOT NULL,
	"C129"	TEXT NOT NULL,
	"C13"	TEXT NOT NULL,
	"C130"	TEXT NOT NULL,
	"C131"	TEXT NOT NULL,
	"C132"	TEXT NOT NULL,
	"C133"	TEXT NOT NULL,
	"C134"	TEXT NOT NULL,
	"C135"	TEXT NOT NULL,
	"C136"	TEXT NOT NULL,
	"C137"	TEXT NOT NULL,
	"C14"	TEXT NOT NULL,
	"C15"	TEXT NOT NULL,
	"C16"	TEXT NOT NULL,
	"C17"	TEXT NOT NULL,
	"C18"	TEXT NOT NULL,
	"C19"	TEXT NOT NULL,
	"C2"	TEXT NOT NULL,
	"C20"	TEXT NOT NULL,
	"C21"	TEXT NOT NULL,
	"C22"	TEXT NOT NULL,
	"C23"	TEXT NOT NULL,
	"C24"	TEXT NOT NULL,
	"C25"	TEXT NOT NULL,
	"C26"	TEXT NOT NULL,
	"C27"	TEXT NOT NULL,
	"C28"	TEXT NOT NULL,
	"C29"	TEXT NOT NULL,
	"C3"	TEXT NOT NULL,
	"C30"	TEXT NOT NULL,
	"C31"	TEXT NOT NULL,
	"C32"	TEXT NOT NULL,
	"C33"	TEXT NOT NULL,
	"C34"	TEXT NOT NULL,
	"C35"	TEXT NOT NULL,
	"C36"	TEXT NOT NULL,
	"C37"	TEXT NOT NULL,
	"C38"	TEXT NOT NULL,
	"C39"	TEXT NOT NULL,
	"C4"	TEXT NOT NULL,
	"C40"	TEXT NOT NULL,
	"C41"	TEXT NOT NULL,
	"C42"	TEXT NOT NULL,
	"C43"	TEXT NOT NULL,
	"C44"	TEXT NOT NULL,
	"C45"	TEXT NOT NULL,
	"C46"	TEXT NOT NULL,
	"C47"	TEXT NOT NULL,
	"C48"	TEXT NOT NULL,
	"C49"	TEXT NOT NULL,
	"C5"	TEXT NOT NULL,
	"C50"	TEXT NOT NULL,
	"C51"	TEXT NOT NULL,
	"C52"	TEXT NOT NULL,
	"C53"	TEXT NOT NULL,
	"C54"	TEXT NOT NULL,
	"C55"	TEXT NOT NULL,
	"C56"	TEXT NOT NULL,
	"C57"	TEXT NOT NULL,
	"C58"	TEXT NOT NULL,
	"C59"	TEXT NOT NULL,
	"C6"	TEXT NOT NULL,
	"C60"	TEXT NOT NULL,
	"C61"	TEXT NOT NULL,
	"C62"	TEXT NOT NULL,
	"C63"	TEXT NOT NULL,
	"C64"	TEXT NOT NULL,
	"C65"	TEXT NOT NULL,
	"C66"	TEXT NOT NULL,
	"C67"	TEXT NOT NULL,
	"C68"	TEXT NOT NULL,
	"C69"	TEXT NOT NULL,
	"C7"	TEXT NOT NULL,
	"C70"	TEXT NOT NULL,
	"C71"	TEXT NOT NULL,
	"C72"	TEXT NOT NULL,
	"C73"	TEXT NOT NULL,
	"C74"	TEXT NOT NULL,
	"C75"	TEXT NOT NULL,
	"C76"	TEXT NOT NULL,
	"C77"	TEXT NOT NULL,
	"C78"	TEXT NOT NULL,
	"C79"	TEXT NOT NULL,
	"C8"	TEXT NOT NULL,
	"C80"	TEXT NOT NULL,
	"C81"	TEXT NOT NULL,
	"C82"	TEXT NOT NULL,
	"C83"	TEXT NOT NULL,
	"C84"	TEXT NOT NULL,
	"C85"	TEXT NOT NULL,
	"C86"	TEXT NOT NULL,
	"C87"	TEXT NOT NULL,
	"C88"	TEXT NOT NULL,
	"C89"	TEXT NOT NULL,
	"C9"	TEXT NOT NULL,
	"C90"	TEXT NOT NULL,
	"C91"	TEXT NOT NULL,
	"C92"	TEXT NOT NULL,
	"C93"	TEXT NOT NULL,
	"C94"	TEXT NOT NULL,
	"C95"	TEXT NOT NULL,
	"C96"	TEXT NOT NULL,
	"C97"	TEXT NOT NULL,
	"C98"	TEXT NOT NULL,
	"C99"	TEXT NOT NULL,
	"L1"	TEXT NOT NULL,
	"L10"	TEXT NOT NULL,
	"L11"	TEXT NOT NULL,
	"L12"	TEXT NOT NULL,
	"L13"	TEXT NOT NULL,
	"L15"	TEXT NOT NULL,
	"L16"	TEXT NOT NULL,
	"L17"	TEXT NOT NULL,
	"L18"	TEXT NOT NULL,
	"L19"	TEXT NOT NULL,
	"L2"	TEXT NOT NULL,
	"L20"	TEXT NOT NULL,
	"L21"	TEXT NOT NULL,
	"L22"	TEXT NOT NULL,
	"L27"	TEXT NOT NULL,
	"L3"	TEXT NOT NULL,
	"L32"	TEXT NOT NULL,
	"L33"	TEXT NOT NULL,
	"L4"	TEXT NOT NULL,
	"L5"	TEXT NOT NULL,
	"L6"	TEXT NOT NULL,
	"L7"	TEXT NOT NULL,
	"L8"	TEXT NOT NULL,
	"L9"	TEXT NOT NULL,
	"MsREF"	TEXT NOT NULL,
	"zhonglan"	TEXT NOT NULL,
	PRIMARY KEY("vcf_ID" AUTOINCREMENT)
);