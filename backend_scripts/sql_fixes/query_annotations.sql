SELECT pros_info.ID_full, pros_info.unique_id, kegg_info.kegg, pathway_info.pathway, go_info.go, interpro_info.interpro, pfam_info.pfam FROM pros_info
		LEFT OUTER JOIN go_info ON pros_info.ID_full = go_info.ID_full
		LEFT OUTER JOIN interpro_info ON pros_info.ID_full = interpro_info.ID_full
		LEFT OUTER JOIN kegg_info ON pros_info.ID_full = kegg_info.ID_full
		LEFT OUTER JOIN pathway_info ON pros_info.ID_full = pathway_info.ID_full
		LEFT OUTER JOIN pfam_info ON pros_info.ID_full = pfam_info.ID_full
		WHERE pros_info.ID_full LIKE "MsG1A10000164.01.T01";