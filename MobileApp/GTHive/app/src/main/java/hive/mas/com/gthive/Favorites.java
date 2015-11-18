package hive.mas.com.gthive;

import android.content.Context;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by bvz on 11/18/15.
 */
public class Favorites {

    private static Favorites sFavorites;

    private List<String> mBuildingIds;

    public static Favorites get(Context context) {
        if (sFavorites == null) {
            sFavorites = new Favorites(context);
        }
        return sFavorites;
    }

    private Favorites(Context context) {
        mBuildingIds = new ArrayList<>();

        // Temporary: Load CULC, Sigma Chi
        mBuildingIds.add("166");
        mBuildingIds.add("324");

        // TODO: load favorited building ids from text file
    }

    public void addBuildingId(String bid) {
        mBuildingIds.add(bid);
    }

    public void removeBuildingId(String bid) {
        mBuildingIds.remove(bid);
    }

    /* Getters and Setters */

    public List<String> getBuildingIds() {
        return mBuildingIds;
    }

    public void setBuildingIds(List<String> buildingIds) {
        mBuildingIds = buildingIds;
    }
}
