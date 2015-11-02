package hive.mas.com.gthive;

import android.content.Context;
import android.util.Log;

import com.squareup.okhttp.Callback;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;

/**
 * Created by bvz on 11/1/15.
 */
public class Campus {
    private final String TAG = "CAMPUS";

    private static Campus sCampus;

    private List<Building> mBuildings;

    public static Campus get(Context context) {
        if (sCampus == null) {
            sCampus = new Campus(context);
        }
        return sCampus;
    }

    private Campus(Context context) {
        mBuildings = new ArrayList<>();

        mBuildings = loadBuildings();

        mBuildings = loadRooms(mBuildings);

        // Sort mBuildings Alphabetically
        sortBuildings();

        // Get Occupancies for all buildings
        updateOccupancies();
    }

    public List<Building> getBuildings() {
        return mBuildings;
    }

    public Building getBuilding(String id) {
        for (Building building : mBuildings) {
            if (building.getId().equals(id)) {
                return building;
            }
        }
        return null;
    }

    private String readTxt(String filename) {
        Log.i("readTxt()", filename);
        InputStream in  = null;
        int c;
        String file_contents = "";
        try {
            String file = "assets/" + filename;
            in = this.getClass().getClassLoader().getResourceAsStream(file);

            // real until the end of the stream
            String mLine;
            while ((c = in.read()) != -1) {
                // convert int to character
                file_contents += (char) c;
            }
        } catch (IOException e) {
            //log the exception
            Log.e(TAG + ".readTxt()", e.toString());
        } finally {
            if (in != null) {
                try {
                    in.close();
                } catch (IOException e) {
                    //log the exception
                    Log.e(TAG + ".readTxt()", e.toString());
                }
            }
        }
        Log.i("readTxt().file_contents", file_contents);
        return file_contents;
    }

    private String readBuildingsTxt() {
        String filename = "buildings.txt";
        return readTxt(filename);
    }

    private String readRoomsTxt() {
        String filename = "rooms.txt";
        return readTxt(filename);
    }

    private List<Building> loadBuildings() {
        // Read in Buildings from Text File
        String txt = readBuildingsTxt();

        List<Building> buildings = new ArrayList<>();

        // Parse JSON
        try {
            JSONObject rootJSON = new JSONObject(txt);
            JSONArray buildingsJSON = rootJSON.getJSONArray("buildings");
            for (int i = 0; i < buildingsJSON.length(); i++) {

                JSONObject buildingJSON = buildingsJSON.getJSONObject(i);
                String id = buildingJSON.getString("b_id");
                String name = buildingJSON.getString("name");

                Building building = new Building(id, name);
                buildings.add(building);
            }
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }
        return buildings;
    }

    private List<Building> loadRooms(List<Building> buildings) {
        // Read in Buildings from Text File
        String txt = readRoomsTxt();

        // Parse JSON
        try {
            JSONObject rootJSON = new JSONObject(txt);
            JSONArray buildingsJSON = rootJSON.getJSONArray("buildings");
            for (int i = 0; i < buildingsJSON.length(); i++) {

                JSONObject buildingJSON = buildingsJSON.getJSONObject(i);

                // Get Building Id
                String bId = buildingJSON.getString("b_id");

                // Load JSON Rooms into List<Room>
                JSONArray jsonRooms = buildingJSON.getJSONArray("rooms");
                List<Room> rooms = new ArrayList<>();
                for (int j = 0; j < jsonRooms.length(); j++) {
                    rooms.add(new Room(bId, jsonRooms.get(j).toString()));
                }

                // Load JSON Floors into List<Floor>
                JSONArray jsonFloors = buildingJSON.getJSONArray("floors");
                List<Floor> floors = new ArrayList<>();
                for (int j = 0; j < jsonFloors.length(); j++) {
                    floors.add(new Floor(bId, jsonFloors.get(j).toString().charAt(0)));
                }

                // Get building object from mBuildings
                Building building = null;
                for (Building b : mBuildings) {
                    if (b.getId().equals(bId)) {
                        building = b;
                        break;
                    }
                }

                if (building != null) {

                    building.setRooms(rooms);
                    building.setFloors(floors);
                } else {
                    Log.i(TAG + ".loadRooms() Building Null", bId);
                }
            }
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }
        return buildings;
    }

    private void sortBuildings() {

        Collections.sort(mBuildings, new Comparator<Building>() {

            @Override
            public int compare(Building b1, Building b2) {
                return b1.getName().compareToIgnoreCase(b2.getName());
            }
        });
    }

    private void updateOccupancies() {
        // https://guides.codepath.com/android/Using-OkHttp
        // Enable Internet Access on Android Emulator: http://stackoverflow.com/questions/20865588/enable-internet-access-on-android-emulator-using-android-studio
        String domain = "http://104.236.76.46:8080";
        String uri = "/api/locationinfo/buildings";
        String url = domain + uri;

        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(url)
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

                try {
                    /* Parse JSON to list out each Building */
                    JSONObject jsonRootObject = new JSONObject(responseData);

                    // Get dictionary of buildings
                    JSONObject jsonBuildingsDictionary = jsonRootObject.optJSONObject("occupancies");
                    Iterator<?> b_ids = jsonBuildingsDictionary.keys();

                    while (b_ids.hasNext()) {
                        String b_id = (String) b_ids.next();
                        if (jsonBuildingsDictionary.get(b_id) instanceof JSONObject) {
                            JSONObject jsonBuilding = (JSONObject) jsonBuildingsDictionary.get(b_id);

                            int occupancy = jsonBuilding.optInt("occupancy");

                            // Update the occupancy of the building
                            getBuilding(b_id).setOccupancy(occupancy);

                            Log.i(TAG, b_id + ": " + occupancy);
                        }
                    }
                }
                catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}
