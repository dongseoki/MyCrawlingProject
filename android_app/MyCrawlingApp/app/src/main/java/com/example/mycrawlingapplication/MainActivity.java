package com.example.mycrawlingapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InputStreamReader;
import java.lang.reflect.Member;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Request;
import okhttp3.Response;
import okhttp3.OkHttpClient;

public class MainActivity extends AppCompatActivity {
    EditText editText;
    TextView textView;
    Handler handler = new Handler();
    ArrayList<LibraryLS> libraryLoanList;
    OkHttpClient client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView =(TextView) findViewById(R.id.textView);
        libraryLoanList = new ArrayList<LibraryLS>();
        client = new OkHttpClient();

    }
    public void ClickButton1(View v){
        Toast.makeText(getApplicationContext(),"버튼을 눌렀습니다.", Toast.LENGTH_LONG).show();
        //String longstr = "{\"boxOfficeResult\":{\"boxofficeType\":\"일별 박스오피스\",\"showRange\":\"20120101~20120101\",\"dailyBoxOfficeList\":[{\"rnum\":\"1\",\"rank\":\"1\",\"rankInten\":\"0\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20112207\",\"movieNm\":\"미션임파서블:고스트프로토콜\",\"openDt\":\"2011-12-15\",\"salesAmt\":\"2776060500\",\"salesShare\":\"36.3\",\"salesInten\":\"-415699000\",\"salesChange\":\"-13\",\"salesAcc\":\"40541108500\",\"audiCnt\":\"353274\",\"audiInten\":\"-60106\",\"audiChange\":\"-14.5\",\"audiAcc\":\"5328435\",\"scrnCnt\":\"697\",\"showCnt\":\"3223\"},{\"rnum\":\"2\",\"rank\":\"2\",\"rankInten\":\"1\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20110295\",\"movieNm\":\"마이 웨이\",\"openDt\":\"2011-12-21\",\"salesAmt\":\"1189058500\",\"salesShare\":\"15.6\",\"salesInten\":\"-105894500\",\"salesChange\":\"-8.2\",\"salesAcc\":\"13002897500\",\"audiCnt\":\"153501\",\"audiInten\":\"-16465\",\"audiChange\":\"-9.7\",\"audiAcc\":\"1739543\",\"scrnCnt\":\"588\",\"showCnt\":\"2321\"},{\"rnum\":\"3\",\"rank\":\"3\",\"rankInten\":\"-1\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20112621\",\"movieNm\":\"셜록홈즈 : 그림자 게임\",\"openDt\":\"2011-12-21\",\"salesAmt\":\"1176022500\",\"salesShare\":\"15.4\",\"salesInten\":\"-210328500\",\"salesChange\":\"-15.2\",\"salesAcc\":\"10678327500\",\"audiCnt\":\"153004\",\"audiInten\":\"-31283\",\"audiChange\":\"-17\",\"audiAcc\":\"1442861\",\"scrnCnt\":\"360\",\"showCnt\":\"1832\"},{\"rnum\":\"4\",\"rank\":\"4\",\"rankInten\":\"0\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20113260\",\"movieNm\":\"퍼펙트 게임\",\"openDt\":\"2011-12-21\",\"salesAmt\":\"644532000\",\"salesShare\":\"8.4\",\"salesInten\":\"-75116500\",\"salesChange\":\"-10.4\",\"salesAcc\":\"6640940000\",\"audiCnt\":\"83644\",\"audiInten\":\"-12225\",\"audiChange\":\"-12.8\",\"audiAcc\":\"895416\",\"scrnCnt\":\"396\",\"showCnt\":\"1364\"},{\"rnum\":\"5\",\"rank\":\"5\",\"rankInten\":\"0\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20113271\",\"movieNm\":\"프렌즈: 몬스터섬의비밀 \",\"openDt\":\"2011-12-29\",\"salesAmt\":\"436753500\",\"salesShare\":\"5.7\",\"salesInten\":\"-89051000\",\"salesChange\":\"-16.9\",\"salesAcc\":\"1523037000\",\"audiCnt\":\"55092\",\"audiInten\":\"-15568\",\"audiChange\":\"-22\",\"audiAcc\":\"202909\",\"scrnCnt\":\"290\",\"showCnt\":\"838\"},{\"rnum\":\"6\",\"rank\":\"6\",\"rankInten\":\"1\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"19940256\",\"movieNm\":\"라이온 킹\",\"openDt\":\"1994-07-02\",\"salesAmt\":\"507115500\",\"salesShare\":\"6.6\",\"salesInten\":\"-114593500\",\"salesChange\":\"-18.4\",\"salesAcc\":\"1841625000\",\"audiCnt\":\"45750\",\"audiInten\":\"-11699\",\"audiChange\":\"-20.4\",\"audiAcc\":\"171285\",\"scrnCnt\":\"244\",\"showCnt\":\"895\"},{\"rnum\":\"7\",\"rank\":\"7\",\"rankInten\":\"-1\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20113381\",\"movieNm\":\"오싹한 연애\",\"openDt\":\"2011-12-01\",\"salesAmt\":\"344871000\",\"salesShare\":\"4.5\",\"salesInten\":\"-107005500\",\"salesChange\":\"-23.7\",\"salesAcc\":\"20634684500\",\"audiCnt\":\"45062\",\"audiInten\":\"-15926\",\"audiChange\":\"-26.1\",\"audiAcc\":\"2823060\",\"scrnCnt\":\"243\",\"showCnt\":\"839\"},{\"rnum\":\"8\",\"rank\":\"8\",\"rankInten\":\"0\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20112709\",\"movieNm\":\"극장판 포켓몬스터 베스트 위시「비크티니와 백의 영웅 레시라무」\",\"openDt\":\"2011-12-22\",\"salesAmt\":\"167809500\",\"salesShare\":\"2.2\",\"salesInten\":\"-45900500\",\"salesChange\":\"-21.5\",\"salesAcc\":\"1897120000\",\"audiCnt\":\"24202\",\"audiInten\":\"-7756\",\"audiChange\":\"-24.3\",\"audiAcc\":\"285959\",\"scrnCnt\":\"186\",\"showCnt\":\"348\"},{\"rnum\":\"9\",\"rank\":\"9\",\"rankInten\":\"0\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20113311\",\"movieNm\":\"앨빈과 슈퍼밴드3\",\"openDt\":\"2011-12-15\",\"salesAmt\":\"137030000\",\"salesShare\":\"1.8\",\"salesInten\":\"-35408000\",\"salesChange\":\"-20.5\",\"salesAcc\":\"3416675000\",\"audiCnt\":\"19729\",\"audiInten\":\"-6461\",\"audiChange\":\"-24.7\",\"audiAcc\":\"516289\",\"scrnCnt\":\"169\",\"showCnt\":\"359\"},{\"rnum\":\"10\",\"rank\":\"10\",\"rankInten\":\"0\",\"rankOldAndNew\":\"OLD\",\"movieCd\":\"20112708\",\"movieNm\":\"극장판 포켓몬스터 베스트 위시 「비크티니와 흑의 영웅 제크로무」\",\"openDt\":\"2011-12-22\",\"salesAmt\":\"125535500\",\"salesShare\":\"1.6\",\"salesInten\":\"-40756000\",\"salesChange\":\"-24.5\",\"salesAcc\":\"1595695000\",\"audiCnt\":\"17817\",\"audiInten\":\"-6554\",\"audiChange\":\"-26.9\",\"audiAcc\":\"235070\",\"scrnCnt\":\"175\",\"showCnt\":\"291\"}]}}";
        RequestThread thread = new RequestThread();
        thread.start();
        //processResponse(longstr);


    }
    String run(String url) throws IOException {
        Request request = new Request.Builder()
                .url(url)
                .build();

        Response response = client.newCall(request).execute();
        return response.body().string();
    }


    class RequestThread extends  Thread{
        public void run(){

            try {
                //String urlStr = "https://us-central1-my-crawling-project.cloudfunctions.net/function-crawling?isbn=9788968481093&title=%28%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A5%BC%20%EC%9C%84%ED%95%9C%29%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B3%BC%ED%95%99&searchFlag=2";
                String urlStr = "https://sddh-crawler-di4on54tsa-uc.a.run.app/?isbn=9788988474839&title=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%EC%84%9D%20%EC%A0%84%EB%AC%B8%EA%B0%80%20%EA%B0%80%EC%9D%B4%EB%93%9C&searchFlag=1";


                Request request = new Request.Builder()
                        .url(urlStr)
                        .build();

                Response response = client.newCall(request).execute();
                String result = response.body().string();
                Log.d("크롤링", "run: " + result);
                processResponse(result);


//                URL url = new URL(urlStr);
//                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
//                if(conn !=null){
//                    conn.setConnectTimeout(10000);
//                    conn.setRequestMethod("GET");
//                    conn.setDoInput(true);
//                    conn.setDoOutput(true);
//
//                    //int resCode = conn.getResponseCode();
//
//                    BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
//                    String line = null;
//                    String result = "";
//                    while(true){
//                        line = reader.readLine();
//                        if(line == null){
//                            break;
//                        }
//                        result += line;
//                        //println(line);
//                    }
//                    Log.d("크롤링 로그", "결과");
//                    processResponse(result);
//                    reader.close();
//                    conn.disconnect();
//                    //Log.d("크롤링 로그", line);
//                }

                Log.d("크롤링 로그", "성공");




            } catch (Exception e){
                e.printStackTrace();
                Log.d("크롤링 로그", "실패");
            }

        }
    }

    public void processResponse(String response){
        Gson gson = new Gson();
        //LibraryLS libraryLoanStatus = gson.fromJson(response, LibraryLS.class);
        //new TypeToken<List<Member>>(){}.getType()
        //출처: https://jekalmin.tistory.com/entry/Gson을-이용한-json을-객체에-담기 [jekalmin의 블로그]
        libraryLoanList = gson.fromJson(response, new TypeToken<ArrayList<LibraryLS>>(){}.getType());
        if(libraryLoanList != null){
            int countLoanStatus = libraryLoanList.size();

            println("size : " + countLoanStatus);
            Log.d("크롤링 로그", "도서관 개수"+countLoanStatus);

            for(int i=0;i <countLoanStatus;i++){

                Log.d("크롤링 로그",""+i + "번 도서관 책 개수 : "+ libraryLoanList.get(i).loanStatusList.size());
                for (int j=0; j<libraryLoanList.get(i).loanStatusList.size();j++){
                    Log.d("크롤링 로그", libraryLoanList.get(i).loanStatusList.get(j).RN);
                    Log.d("크롤링 로그", libraryLoanList.get(i).loanStatusList.get(j).CN);
                    Log.d("크롤링 로그", libraryLoanList.get(i).loanStatusList.get(j).POS);
                    Log.d("크롤링 로그",""+ libraryLoanList.get(i).loanStatusList.get(j).STATE);
                    Log.d("크롤링 로그", libraryLoanList.get(i).loanStatusList.get(j).RDD);
                    Log.d("크롤링 로그", ""+libraryLoanList.get(i).loanStatusList.get(j).BN);
                    Log.d("크롤링 로그", ""+libraryLoanList.get(i).loanStatusList.get(j).errorMessage);
                }

            }
        }
    }

    public void println(final String data){
        handler.post(new Runnable() {
            @Override
            public void run() {
                textView.append(data + "\n");
                Log.d("크롤링 로그", "핸들링 성공");
            }
        });
    }
}
