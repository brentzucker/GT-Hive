package hive.mas.com.gthive;

import android.support.v4.app.Fragment;

/**
 * Created by bvz on 11/1/15.
 */
public class BuildingListActivity extends SingleFragmentActivity {

    @Override
    protected Fragment createFragment() {
        return new BuildingListFragment();
    }
}
