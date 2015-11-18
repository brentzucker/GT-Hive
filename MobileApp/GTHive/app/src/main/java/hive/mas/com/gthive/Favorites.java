package hive.mas.com.gthive;

import android.content.Context;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Created by bvz on 11/18/15.
 */
public class Favorites {

    private static Favorites sFavorites;

    private Set<String> mBuildingIds;

    public static Favorites get(Context context) {
        if (sFavorites == null) {
            sFavorites = new Favorites(context);
        }
        return sFavorites;
    }

    private Favorites(Context context) {
        mBuildingIds = new HashSet<>();

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

        List<String> buildingIds = new ArrayList<>();
        buildingIds.addAll(mBuildingIds);
        return buildingIds;
    }

    public void setBuildingIds(Set<String> buildingIds) {
        mBuildingIds = buildingIds;
    }
}
