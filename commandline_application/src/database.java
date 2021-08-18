import java.io.File;
import java.sql.*;
import org.sqlite.JDBC;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;

public class database {
  // given a DNA seq, return its conjugate seq
  private static String get_conjugate(String seq) {
    String ans = "";
    for (int i = seq.length() - 1; i >= 0; i--) {
      if (seq.charAt(i) == 'A')
        ans += 'T';
      else if (seq.charAt(i) == 'T')
        ans += 'A';
      else if (seq.charAt(i) == 'C')
        ans += 'G';
      else if (seq.charAt(i) == 'G')
        ans += 'C';
    }
    return ans;
  }

  public static void main(String[] args) {
    try {
      // database setup
      Scanner sc = new Scanner(System.in);
      String dbPath = "./Alfalfa.db";
      File dbFile = new File(dbPath);
      while (!dbFile.exists()) {
        System.out.println("*** Alfalfa.db is not found under the current path: ***");
        System.out.println("*** " + dbPath + " ***");
        System.out.println("*** Please enter a correct path to Alfalfa.db: ***");
        System.out.print("> ");
        dbPath = sc.nextLine();
        while (!dbPath.contains("/Alfalfa.db")) {
          System.out
              .println("*** The path, absolute or relative, should ends by \"/Alfalfa.db\" ***");
          System.out.print("> ");
          dbPath = sc.nextLine();
        }
        dbFile = new File(dbPath);
      }
      String sql = "jdbc:sqlite:" + dbPath;
      Class.forName("org.sqlite.JDBC");
      Connection conn = DriverManager.getConnection(sql);
      Statement stat = conn.createStatement();
      ResultSet rs;
      int cnt = 0;

      // query app
      while (true) {
        // repeat these prompts after each query until option C is selected
        System.out
            .println("**********************************************************************");
        System.out.println("Welcome to the Alfalfa database, please select an option:");
        System.out.println("[A] Query about all information in Alfalfa.db related to a gene ID");
        System.out.println("[B] Query about IDs of all genes whose annotations include a keywords");
        System.out.println("[C] Query about all variations between two points on a chromosome");
        System.out.println("[D] Exit");
        System.out.print("> ");
        String option = sc.nextLine();

        // exit app
        if (option.substring(0, 1).toUpperCase().equals("D")) {
          System.out.println("Thank you for using the Alfalfa database.");
          System.out
              .println("**********************************************************************");
          break;
        }

        // query mode A
        if (option.substring(0, 1).toUpperCase().equals("A")) {
          System.out.println("Please enter a ID:");
          System.out.print("> ");
          String query_id = sc.nextLine();

          // check validity of query_id, process it if needed
          String extension; // "" if no extension
          extension = "";
          if (query_id.length() == 16) {
            query_id = query_id.substring(0, 13); // all records in gff have .01
            // extension = "";
          } else if (query_id.length() == 20) {
            // separate main ID and its extension
            extension = query_id.substring(13);
            query_id = query_id.substring(0, 13);
          } else if (query_id.length() != 13) {
            System.out.println("*** The ID should have 13, 16, or 20 characters ***");
            continue;
          }

          // query annotate_info
          rs = stat.executeQuery(
              "SELECT * FROM annotate_info WHERE ID_full LIKE \"" + query_id + extension + "%\";");
          cnt = 0;
          while (rs.next()) {
            if (cnt == 0)
              System.out.println("*** Results from annotate_info: ***");
            cnt++;
            System.out.print("id_full = " + rs.getString("id_full") + ", ");
            System.out.print("db_name = " + rs.getString("db_name") + ", ");
            System.out.print("info1 = " + rs.getString("info1") + ", ");
            System.out.println("info2 = " + rs.getString("info2"));
          }
          if (cnt > 0)
            System.out.println("*** " + cnt + " related annotate_info were returned above ***\n");

          // query go_info, interpro_info, kegg_info, pathway_info, and pfam_info
          rs = stat.executeQuery(
              "SELECT pros_info.ID_full, pros_info.unique_id, kegg_info.kegg, pathway_info.pathway,"
                  + " go_info.go, interpro_info.interpro, pfam_info.pfam FROM pros_info\n"
                  + "    LEFT OUTER JOIN go_info ON pros_info.ID_full = go_info.ID_full\n"
                  + "    LEFT OUTER JOIN interpro_info ON pros_info.ID_full = interpro_info.ID_full\n"
                  + "    LEFT OUTER JOIN kegg_info ON pros_info.ID_full = kegg_info.ID_full\n"
                  + "    LEFT OUTER JOIN pathway_info ON pros_info.ID_full = pathway_info.ID_full\n"
                  + "    LEFT OUTER JOIN pfam_info ON pros_info.ID_full = pfam_info.ID_full\n"
                  + "    WHERE pros_info.ID_full LIKE \"" + query_id + extension + "%\";");
          cnt = 0;
          while (rs.next()) {
            if (rs.getString("go") != null || rs.getString("interpro") != null
                || rs.getString("kegg") != null || rs.getString("pathway") != null
                || rs.getString("pfam") != null) {
              if (cnt == 0)
                System.out.println("*** Annotations from other databases: ***");
              cnt++;
              System.out.println("< id_full = " + rs.getString("id_full") + " >");
              System.out.println("go = " + rs.getString("go"));
              System.out.println("interpro = " + rs.getString("interpro"));
              System.out.println("kegg = " + rs.getString("kegg"));
              System.out.println("pathway = " + rs.getString("pathway"));
              System.out.println("pfam = " + rs.getString("pfam"));
            }
          }
          if (cnt > 0)
            System.out
                .println("*** Related annotations from other databases were returned above ***\n");

          // query pros_info
          rs = stat.executeQuery(
              "SELECT * FROM pros_info WHERE ID_full LIKE \"" + query_id + extension + "%\";");
          cnt = 0;
          while (rs.next()) {
            if (cnt == 0)
              System.out.println("*** Results from pros_info database: ***");
            cnt++;
            System.out.print("id_full = " + rs.getString("id_full") + ", ");
            System.out.println("pros = " + rs.getString("pros"));
          }
          if (cnt > 0)
            System.out.println("*** " + cnt + " related pros_info were returned above ***\n");

          // query gff
          rs = stat.executeQuery("SELECT * FROM gff AS G, ID_to_uniqueid AS I WHERE I.ID =\""
              + query_id + "\" AND G.unique_id >= I.start AND G. unique_id <= I.end;");
          cnt = 0;
          while (rs.next()) {
            if (!extension.equals("")) {
              String full_id = query_id + extension;
              String rst_id = rs.getString("attributes");
              if (!rst_id.contains(full_id))
                continue;
            }
            if (cnt == 0)
              System.out.println("*** Results from gff: ***");
            cnt++;
            System.out.print("seqid = " + rs.getString("seqid") + ", ");
            System.out.print("source = " + rs.getString("source") + ", ");
            System.out.print("type = " + rs.getString("type") + ", ");
            System.out.print("start = " + rs.getString("start") + ", ");
            System.out.print("end = " + rs.getString("end") + ", ");
            System.out.print("score = " + rs.getString("score") + ", ");
            System.out.print("strand = " + rs.getString("strand") + ", ");
            System.out.print("phase = " + rs.getString("phase") + ", ");
            System.out.print("attributes = " + rs.getString("attributes") + ", ");
            String dna = rs.getString("DNA");
            // replace by DNA conjugates when needed
            if (rs.getString("strand").equals("-"))
              dna = get_conjugate(dna);
            System.out.println("DNA = " + dna);
          }
          if (cnt > 0)
            System.out.println("*** " + cnt
                + " related gff records and their DNA sequences were returned above ***");
          else
            System.out.println("*** NO related information was found in the Alfalfa database ***");
          rs.close();
        }

        // query mode B
        if (option.substring(0, 1).toUpperCase().equals("B")) {
          System.out.println("Please enter some keywords:");
          System.out.print("> ");
          String keywords = sc.nextLine();
          rs = stat.executeQuery("SELECT * FROM annotate_info WHERE info1 LIKE \"%" + keywords
              + "%\" OR info2 LIKE \"%" + keywords + "%\";");
          cnt = 0;
          int number_of_unique_id = 0;
          HashSet<String> my_set = null;
          while (rs.next()) {
            if (cnt == 0) {
              my_set = new HashSet<String>();
              number_of_unique_id = 0;
            }
            cnt++;
            if (my_set.add(rs.getString("id_full")))
              number_of_unique_id++;
            System.out.print("id_full = " + rs.getString("id_full") + ", ");
            System.out.print("db_name = " + rs.getString("db_name") + ", ");
            System.out.print("info1 = " + rs.getString("info1") + ", ");
            System.out.println("info2 = " + rs.getString("info2"));
          }
          if (cnt > 0) {
            System.out.println("*** " + cnt + " related annotate_info were returned above ***");
            System.out.println("*** " + number_of_unique_id + " unique gene IDs involved: ***");
            if (my_set != null && !my_set.isEmpty())
              System.out.println(my_set.toString());
          } else
            System.out.println("*** NO related information was found in the Alfalfa database ***");
          rs.close();
        }

        // query mode C
        if (option.substring(0, 1).toUpperCase().equals("C")) {
          System.out.println("Please enter a chromosome number (an integer between 1 and 8):");
          System.out.print("> ");
          int num;
          try {
            num = Integer.parseInt(sc.nextLine());
            if (num < 1 || num > 8) {
              System.out.println("*** The chromosome number entered was invalid ***");
              continue;
            }
          } catch (NumberFormatException e) {
            System.out.println("*** The chromosome number entered was invalid ***");
            continue;
          }

          // values from get_max_vcfID.sql and get_min_vcfIDs.sql
          int max_pos = 148124263;
          int arr[] = {1, 17551074, 32991065, 52346699, 69388115, 89626087, 113452234, 132015073,
              max_pos + 1};

          int vcf_ID_lower_bound = arr[num - 1];
          int vcf_ID_upper_bound = arr[num] - 1;
          int POS_lower_bound;
          int POS_upper_bound;

          try {
            System.out.println("Please enter a lower bound of POS (a positive integer):");
            System.out.print("> ");
            POS_lower_bound = Integer.parseInt(sc.nextLine());
            if (POS_lower_bound < 1) {
              System.out.println("*** The lower bound entered was invalid ***");
              continue;
            }

            System.out.println("Please enter a upper bound of POS (a positive integer):");
            System.out.print("> ");
            POS_upper_bound = Integer.parseInt(sc.nextLine());
            if (POS_upper_bound < 1) {
              System.out.println("*** The upper bound entered was invalid ***");
              continue;
            }
          } catch (NumberFormatException e) {
            System.out.println("*** The entered String was not an Integer ***");
            continue;
          }

          // query vcf
          rs = stat.executeQuery("SELECT * FROM vcf WHERE vcf_ID BETWEEN " + vcf_ID_lower_bound
              + " AND " + vcf_ID_upper_bound + " AND POS BETWEEN " + POS_lower_bound + " AND "
              + POS_upper_bound + ";");

          cnt = 0;
          ResultSetMetaData rsmd = rs.getMetaData();
          int columnsNumber = rsmd.getColumnCount();
          while (rs.next()) {
            cnt++;
            for (int i = 1; i <= columnsNumber; i++) {
              if (i > 1)
                System.out.print(",  ");
              String columnValue = rs.getString(i);
              System.out.print(rsmd.getColumnName(i) + " = " + columnValue);
            }
            System.out.println();
          }
          System.out.println("*** " + cnt + " related VCF records were returned above ***");
        }
      }

      // close database
      sc.close();
      conn.close();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
