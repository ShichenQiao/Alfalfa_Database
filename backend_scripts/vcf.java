import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class vcf {

  public static void main(String[] args) throws IOException {
    String vcf = args[0];   // Usage: java vcf <path_to_vcf>
    FileInputStream fis = new FileInputStream(vcf);
    BufferedReader br = new BufferedReader(new InputStreamReader(fis));
    String line = null;
    int cnt = 1; // vcf_ID
    while ((line = br.readLine()) != null) {
      // ignore file headers and column names
      if (line.length() == 0 || line.charAt(0) == '#')
        continue;
      String[] strArrays = line.split("\\s+");
      StringBuilder fullLine = new StringBuilder();
      int i = 9;

      // Read variation info
      fullLine.append(strArrays[0]); // CHROM
      fullLine.append("\t");
      fullLine.append(strArrays[1]); // POS
      fullLine.append("\t");
      fullLine.append(strArrays[3]); // REF
      fullLine.append("\t");
      fullLine.append(strArrays[4]); // ALT
      fullLine.append("\t");

      // Split REF into lists
      ArrayList<String> ref = new ArrayList<String>();
      ref.add(strArrays[3]);
      String[] s2 = strArrays[4].split(",");
      for (String s1 : s2) {
        ref.add(s1);
      }

      // Replace */* notations to <seq>/<seq> notation
      while (i < 172) {
        String[] sa = strArrays[i].split(":");
        ++i;
        String[] sc = sa[0].split("/");
        if (sa[0].equals("./.")) {
          fullLine.append("./.");
        } else {
          int t1 = Integer.parseInt(sc[0]);
          int t2 = Integer.parseInt(sc[1]);
          // Get correct REF sequences from the ArrayList
          fullLine.append(ref.get(t1) + "/" + ref.get(t2));
        }
        fullLine.append("\t");
      }

      // Generate sql INSERT statement for the current variation record
      String sql =
          "INSERT INTO vcf(vcf_ID,CHROM,POS,REF,ALT,C1,C10,C100,C101,C102,C103,C104,C105,C106,"
              + "C107,C108,C109,C11,C110,C111,C112,C113,C114,C115,C116,C117,C118,C119,C12,C120,"
              + "C121,C122,C123,C124,C125,C126,C127,C128,C129,C13,C130,C131,C132,C133,C134,C135,"
              + "C136,C137,C14,C15,C16,C17,C18,C19,C2,C20,C21,C22,C23,C24,C25,C26,C27,C28,C29,"
              + "C3,C30,C31,C32,C33,C34,C35,C36,C37,C38,C39,C4,C40,C41,C42,C43,C44,C45,C46,C47,"
              + "C48,C49,C5,C50,C51,C52,C53,C54,C55,C56,C57,C58,C59,C6,C60,C61,C62,C63,C64,C65,"
              + "C66,C67,C68,C69,C7,C70,C71,C72,C73,C74,C75,C76,C77,C78,C79,C8,C80,C81,C82,C83,"
              + "C84,C85,C86,C87,C88,C89,C9,C90,C91,C92,C93,C94,C95,C96,C97,C98,C99,L1,L10,L11,"
              + "L12,L13,L15,L16,L17,L18,L19,L2,L20,L21,L22,L27,L3,L32,L33,L4,L5,L6,L7,L8,L9,"
              + "MsREF,zhonglan) VALUES(" + cnt++ + ",";
      String[] x = fullLine.toString().split("\t");
      for (String element : x) {
        sql += "\"" + element + "\",";
      }
      sql = sql.substring(0, sql.length() - 1);
      sql += ");";
      System.out.println(sql); // save to output .sql file
    }

    fis.close();
  }
}

