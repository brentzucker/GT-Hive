package hive.mas.com.gthive;

/**
 * Created by bvz on 11/1/15.
 */
public class Building {

    private String mId;
    private String mName;

    public Building(String id, String name) {
        mId = id;
        mName = name; // Eventually load name from buildings.txt
    }

    public String getId() {
        return mId;
    }

    public String getName() {
        return mName;
    }

    public void setId(String id) {
        mId = id;
    }

    public void setName(String name) {
        mName = name;
    }
}
