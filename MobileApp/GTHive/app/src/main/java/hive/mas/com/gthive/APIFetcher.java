package hive.mas.com.gthive;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Iterator;

/**
 * Created by bvz on 11/13/15.
 */
public class APIFetcher {

    private static final String TAG = "APIFetcher";

    public byte[] getUrlBytes(String urlSpec) throws IOException {
        URL url = new URL(urlSpec);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        try {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            InputStream in = connection.getInputStream();

            if (connection.getResponseCode() != HttpURLConnection.HTTP_OK) {
                throw new IOException(connection.getResponseMessage() + ": with" + urlSpec);
            }

            int bytesRead = 0;
            byte[] buffer = new byte[1024];
            while ((bytesRead = in.read(buffer)) > 0) {
                out.write(buffer, 0, bytesRead);
            }
            out.close();
            return out.toByteArray();
        } finally {
            connection.disconnect();
        }
    }

    public String getUrlString(String urlSpec) throws IOException {
        return new String(getUrlBytes(urlSpec));
    }

    public Campus fetchBuildingOccupancies(Campus campus) {

        String domain = "http://104.236.76.46:8080";
        String uri = "/api/locationinfo/buildings";
        String url = domain + uri;

        try {
            String jsonString = getUrlString(url);
            Log.i(TAG, "Received JSON: " + jsonString);
            JSONObject jsonBody = new JSONObject(jsonString);
            parseBuildingOccupancies(campus, jsonBody);
        } catch (JSONException je) {
            Log.e(TAG, "Failed to parse JSON", je);
        } catch (IOException ioe) {
            Log.e(TAG, "Failed to fetch items", ioe);
        }

        return campus;
    }

    private void parseBuildingOccupancies(Campus campus, JSONObject jsonBody) throws IOException, JSONException {
        JSONObject occupanciesJsonObject = jsonBody.optJSONObject("occupancies");
        Iterator<?> b_ids = occupanciesJsonObject.keys();

        while (b_ids.hasNext()) {
            String b_id = (String) b_ids.next();
            if (occupanciesJsonObject.get(b_id) instanceof JSONObject) {
                JSONObject buildingJsonObject = (JSONObject) occupanciesJsonObject.get(b_id);

                int occupancy = buildingJsonObject.getInt("occupancy");

                // Update the occupancy of the building
                campus.getBuilding(b_id).setOccupancy(occupancy);

                Log.i(TAG, b_id + ": " + occupancy);
            }
        }
    }
}
