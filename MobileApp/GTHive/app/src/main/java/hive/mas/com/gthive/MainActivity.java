package hive.mas.com.gthive;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import com.squareup.okhttp.Callback;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        /* * * * * * * * * * * * * * * * * * * * * * *
         * Change Text View to JSON from API Endpoint
         * * * * * * * * * * * * * * * * * * * * * * */

        // https://guides.codepath.com/android/Using-OkHttp
        // Enable Internet Access on Android Emulator: http://stackoverflow.com/questions/20865588/enable-internet-access-on-android-emulator-using-android-studio
        String api_buildings = "http://104.236.76.46:8080/api/building_ids_names_local";

        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(api_buildings)
                .build();

        client.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(Request request, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(final Response response) throws IOException {

                // Read data on the worker thread
                final String responseData = response.body().string();

                // Run view-related code back on the main thread
                MainActivity.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        TextView mTextView = (TextView) findViewById(R.id.web_data_text);

                        try {
                            /* Parse JSON to list out each Building */
                            JSONObject jsonRootObject = new JSONObject(responseData);

                            // Get array of buildings
                            JSONArray jsonArray = jsonRootObject.optJSONArray("buildings");

                            for (int i = 0; i < jsonArray.length(); i++) {
                                JSONObject jsonObject = jsonArray.getJSONObject(i);

                                String b_id = jsonObject.optString("b_id").toString();
                                String name = jsonObject.optString("name").toString();

                                // Append Building info to UI element, TextView
                                mTextView.append(name + ": " + b_id + "\n");
                            }
                        }
                        catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
