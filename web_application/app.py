from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# given a DNA seq, return its conjugate seq
def get_conjugate(seq):
    rev = str(seq)[::-1]
    ans = ""
    for i in range(0, len(rev)):
        if rev[i] == 'A':
            ans += 'T'
        elif rev[i] == 'T':
            ans += 'A'
        elif rev[i] == 'C':
            ans += 'G'
        elif rev[i] == 'G':
            ans += 'C'
    return ans

# home page with input place holders
@app.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html', show_place_holder=True)

# query mode A, ID search
@app.route('/ID/', methods = ['POST', 'GET'])
def mode_A():
    if request.method == 'POST':
        id = request.form['content1']   # gene ID input from html

        if len(id) != 13 and len(id) != 16 and len(id) != 20:
            return render_template('error.html', err_msg="Input gene ID was invalid.")

        conn = sqlite3.connect("./static/sql/Alfalfa.db")
        cu = conn.cursor()

        # query pros_info
        sql = "SELECT * FROM pros_info WHERE ID_full LIKE \"" + id + "%\";"
        cu.execute(sql)
        pros_infos = cu.fetchall()

        if len(pros_infos) == 0:
            return render_template('error.html', err_msg="Gene ID not found")

        # query annotate_info
        sql = "SELECT * FROM annotate_info WHERE ID_full LIKE \"" + id + "%\";"
        cu.execute(sql)
        annotate_infos = cu.fetchall()

        show_annotate = True
        if len(annotate_infos) == 0:
            show_annotate = False

        # query go_info, interpro_info, kegg_info, pathway_info, and pfam_info
        have_info = False

        pri_id = id
        if len(id) != 13:
            pri_id = id[0:13]

        sql = "SELECT pros_info.ID_full, pros_info.unique_id, kegg_info.kegg, pathway_info.pathway,"
        sql += " go_info.go, interpro_info.interpro, pfam_info.pfam FROM pros_info\n"
        sql += "    LEFT OUTER JOIN go_info ON pros_info.ID_full = go_info.ID_full\n"
        sql += "    LEFT OUTER JOIN interpro_info ON pros_info.ID_full = interpro_info.ID_full\n"
        sql += "    LEFT OUTER JOIN kegg_info ON pros_info.ID_full = kegg_info.ID_full\n"
        sql += "    LEFT OUTER JOIN pathway_info ON pros_info.ID_full = pathway_info.ID_full\n"
        sql += "    LEFT OUTER JOIN pfam_info ON pros_info.ID_full = pfam_info.ID_full\n"
        sql += "    WHERE pros_info.ID_full LIKE \"" + pri_id + "%\";"
        cu.execute(sql)
        infos = cu.fetchall()

        # filter infos, only keep rows with at least one annotation that is not None
        info = []
        for x in infos:
            for i in range(2, 7):
                if x[i] != None:
                    info = x
                    break

        # process kegg
        kegg_list = None
        if len(info) > 0:
            if info[2] != None:
                kegg_list = str(info[2]).split(";")
        if kegg_list != None:
            for i in range(0, len(kegg_list)):
                kegg_list[i] = kegg_list[i][6:]
            have_info = True

        # process pathway
        temp_list = None
        pathway_list = []
        if len(info) > 0:
            if info[3] != None:
                temp_list = str(info[3]).split(";")
        if temp_list != None:
            for i in range(0, len(temp_list)):
                # exclude KEGG duplicates
                if not ("KEGG" in temp_list[i][0:4]):
                    pathway_list.append(temp_list[i])
        if len(pathway_list) == 0:
            pathway_list = None
        else:
            have_info = True

        # process go
        go_list = None
        if len(info) > 0:
            if info[4] != None:
                go_list = str(info[4]).split(";")
        if go_list != None:
            for i in range(0, len(go_list)):
                go_list[i] = go_list[i][3:]
            have_info = True

        # process interpro
        interpro_list = None
        if len(info) > 0:
            if info[5] != None:
                interpro_list = str(info[5]).split("|")
        if interpro_list != None:
            have_info = True
                
        # process pfam
        pfam_list = None
        if len(info) > 0:
            if info[6] != None:
                pfam_list = str(info[6]).split(";")
        if pfam_list != None:
            have_info = True

        # get 16-character gene ID
        gene_ID = None
        if have_info:
            gene_ID = str(info[0])[0:16]

        # query gff
        sql = "SELECT * FROM gff AS G, ID_to_uniqueid AS I WHERE I.ID =\"" + pri_id + "\" AND G.unique_id >= I.start AND G. unique_id <= I.end;"
        cu.execute(sql)
        temp_list = cu.fetchall()
        gffs = []
        for x in temp_list:
            if id in x[9]:
                gffs.append(x)
        
        # replace by DNA conjugates when needed
        for i in range(0, len(gffs)):
            if gffs[i][7] == "-":
                temp = list(gffs[i])
                temp[10] = get_conjugate(temp[10])
                gffs[i] = tuple(temp)

        # add combined CDS sequences to pros_info
        cds = []
        for x in gffs:
            if x[3] == "CDS":
                cds.append(x)
        for i in range(0, len(pros_infos)):
            cds_combined = ""
            for x in cds:
                if str(pros_infos[0][1]) in str(x[9]):
                    cds_combined += x[10]
            temp_list = list(pros_infos[i])
            temp_list.append(cds_combined)
            pros_infos[i] = tuple(temp_list)

        # get transcriptome data from Table alltpm
        sql = "SELECT * FROM alltpm WHERE GeneID = \"" + pri_id + ".01\";"
        cu.execute(sql)
        temp_list = cu.fetchall()[0]
        transcriptome_list = []
        for i in range(1, len(temp_list)):
            transcriptome_list.append(temp_list[i])

        # print to html page
        if show_annotate:
            if have_info:
                return render_template('home.html', mode="A", id=id, show_annotate=show_annotate, annotate_infos=annotate_infos, temp=annotate_infos[0], annotate_span=len(annotate_infos)+1, gene_ID=gene_ID, have_info=have_info, kegg_list=kegg_list, pathway_list=pathway_list, go_list=go_list, interpro_list=interpro_list, pfam_list=pfam_list, pros_infos=pros_infos, gffs=gffs, len_gff=len(gffs), transcriptome_list=transcriptome_list)
            else:
                return render_template('home.html', mode="A", id=id, show_annotate=show_annotate, annotate_infos=annotate_infos, temp=annotate_infos[0], annotate_span=len(annotate_infos)+1, have_info=have_info, pros_infos=pros_infos, gffs=gffs, len_gff=len(gffs), transcriptome_list=transcriptome_list)
        else:
            if have_info:
                return render_template('home.html', mode="A", id=id, show_annotate=show_annotate, gene_ID=gene_ID, have_info=have_info, kegg_list=kegg_list, pathway_list=pathway_list, go_list=go_list, interpro_list=interpro_list, pfam_list=pfam_list, pros_infos=pros_infos, gffs=gffs, len_gff=len(gffs), transcriptome_list=transcriptome_list)
            else:
                return render_template('home.html', mode="A", id=id, show_annotate=show_annotate, have_info=have_info, pros_infos=pros_infos, gffs=gffs, len_gff=len(gffs), transcriptome_list=transcriptome_list)
    return redirect('/')

# query mode B, keywords search
@app.route('/annotation/', methods = ['POST', 'GET'])
def mode_B():
    if request.method == 'POST':
        keywords = request.form['content2']    # keywords input from html

        if len(keywords) < 1:
            return render_template('error.html', err_msg="No keywords entered.")

        # query annotate_info
        conn = sqlite3.connect("./static/sql/Alfalfa.db")
        cu = conn.cursor()
        sql = "SELECT * FROM annotate_info WHERE info1 LIKE \"%" + keywords + "%\" OR info2 LIKE \"%" + keywords + "%\";"
        cu.execute(sql)
        ans_list = cu.fetchall()

        if len(ans_list) == 0:
            return render_template('error.html', err_msg="No such keywords found in annotation records.")

        # conbine rows with the same gene ID by calculating rowspan value for html
        rowspan = []
        temp = ans_list[0][0]
        cnt = 0
        l = 0
        for ans in ans_list:
            if ans[0] == temp:
                cnt += 1
            else:
                if len(rowspan) == 0:
                    rowspan.append(cnt)
                    for i in range(1, cnt):
                        rowspan.append(0)
                else:
                    l += 1
                    rowspan.append(cnt + 1)
                    for i in range(1, cnt + 1):
                        rowspan.append(0)
                temp = ans[0]
                cnt = 0
        rowspan.append(len(ans_list) - len(rowspan))
        for i in range(0, len(ans_list) - len(rowspan)):
            rowspan.append(0)
        
        # add rowspan information to each row of query results
        for i in range(0, len(ans_list)):
            temp_list = []
            temp_list.append(rowspan[i])
            ans_list[i] += tuple(temp_list)

        # print to html page
        for i in range(0, len(keywords)):
            if keywords[i] == " ":
                keywords[i] == "~"
        return render_template('home.html', mode="B", keywords=keywords, ans_list=ans_list, l=l + 2)
    return redirect('/')

# query mode C, VCF search
@app.route('/VCF/', methods = ['POST', 'GET'])
def mode_C():
    if request.method == 'POST':
        seqid = request.form['content3']     # seqid input from html
        low = request.form['content4']   # low input from html
        high = request.form['content5']  # high input from html

        if len(seqid) != 4 or len(low) < 1 or len(high) < 1 or int(low) < 1 or int(high) < 1 or int(low) >= int(high):
            return render_template('error.html', err_msg="Invalid VCF query.")

        # default range is set to be 1 ~ 3000 bp
        if int(high) - int(low) >= 3000:
            return render_template('error.html', err_msg="Please select a range that is less than or equals to 3000bp.")

        conn = sqlite3.connect("./static/sql/Alfalfa.db")
        cu = conn.cursor()

        # setup ranges from sql results
        max_pos = 148124263  # get_max_vcfID.sql
        arr = [1, 17551074, 32991065, 52346699, 69388115, 89626087, 113452234, 132015073, max_pos + 1]  # get_min_vcfIDs.sql
        
        # get a smaller vcf_ID range to query from
        temp_low = str(arr[int(seqid[3:]) - 1])
        temp_high = str(arr[int(seqid[3:])] - 1)
        sql = "SELECT vcf_ID FROM vcf_jump_table WHERE vcf_ID BETWEEN " + temp_low + " AND " + temp_high + " AND POS <= " + low + " ORDER BY vcf_ID DESC LIMIT 1;"
        cu.execute(sql)
        temp = cu.fetchall()
        start = str(temp_low)
        if len(temp) != 0:
            start = str(list(temp[0])[0])
        sql = "SELECT vcf_ID FROM vcf_jump_table WHERE vcf_ID BETWEEN " + temp_low + " AND " + temp_high + " AND POS >= " + high + " LIMIT 1;"
        cu.execute(sql)
        temp = cu.fetchall()
        end = str(temp_high)
        if len(temp) != 0:
            end = str(list(temp[0])[0])

        # query VCF records
        sql = "SELECT * FROM vcf WHERE vcf_ID BETWEEN " + start + " AND " + end + " AND POS BETWEEN " + low + " AND " + high + ";"
        cu.execute(sql)
        vcfs = cu.fetchall()

        if len(vcfs) == 0:
            return render_template('error.html', err_msg="No VCF entry found.")

        # get DNA sequence between low and high
        file_name = "./static/DNA/" + seqid + ".txt"
        f = open(file_name, 'r')
        data = f.read()
        f.close()
        seq = data[int(low) - 1:int(high)]

        # print to html page
        return render_template('home.html', mode="C", seqid=int(seqid[3:]), low=low, high=high, length=len(seq), DNA=seq, vcfs=vcfs, l=len(vcfs))
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug = True)