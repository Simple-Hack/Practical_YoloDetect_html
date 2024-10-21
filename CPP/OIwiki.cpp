#include<format>
#include<iostream>
#include<vector>
#include<iostream>
#include<functional>
#include<queue>
#include<unordered_map>
#include<print>
#include<version>
class Solution {
private:
	int N = 510;
	std::vector<int> father, sz;
	std::vector<std::pair<int, int>> direction = { {-1,0},{1,0},{0,-1},{0,1} };

	int find( int x ) {
		return father[x] == x ? x : father[x] = find( father[x] );
	}

	void merge( int x, int y ) {
		int father_x = find( x );
		int father_y = find( y );
		if (father_x == father_y) return;
		if (sz[father_x] > sz[father_y]) {
			sz[father_x] += sz[father_y];
			father[father_y] = father_x;
		}
		else {
			sz[father_y] += sz[father_x];
			father[father_x] = father_y;
		}
	}
public:
	int largestIsland( std::vector<std::vector<int>>& grid ) {
		father = std::vector<int>( );
		sz = std::vector<int>( );
		father.resize( grid.size( ) * grid.size( ), 0 );
		sz.resize( grid.size( ) * grid.size( ), 1 );
		for (int i = 0;i < grid.size( ) * grid.size( );i++) father[i] = i;

		for (int i = 0;i < grid.size( );i++) {
			for (int j = 0;j < grid.size( );j++) {
				if (grid[i][j] == 0) continue;
				for (auto [dx, dy] : direction) {
					if (i + dx >= 0 and i + dx < grid.size( ) and j + dy >= 0 and j + dy < grid.size( )
						and grid[i + dx][j + dy] == 1) {
						merge( i * grid.size( ) + j, (i + dx) * grid.size( ) + j + dy );
					}
				}
			}
		}
		int ans = 0;
		for (int i = 0;i < grid.size( );i++) {
			for (int j = 0;j < grid[0].size( );j++) {
				if (grid[i][j] == 1)
					ans = std::max( ans, sz[find( i * grid[0].size( ) + j )] );
				else {
					int curArea = 0;
					std::vector<int> visitedFather;
					for (auto [dx, dy] : direction) {
						if (i + dx >= 0 and i + dx < grid.size( ) and j + dy >= 0 and j + dy < grid[0].size( )
							and std::find( visitedFather.begin( ), visitedFather.end( ), find( (i + dx) * grid[0].size( ) + j + dy ) ) == visitedFather.end( )
							and grid[i + dx][j + dy] == 1) {
							visitedFather.push_back( find( (i + dx) * grid[0].size( ) + j + dy ) );
							curArea += sz[find( (i + dx) * grid[0].size( ) + j + dy )];
						}
					}
					ans = std::max( ans, curArea + 1 );
				}
			}
		}
		return ans;
	}
};

int main( ) {
	std::vector<std::vector<int>> grid = { {1,0},{0,1} };
	Solution s;
	s.largestIsland( grid );
    std::cout << "Compiler version: " << __cplusplus << std::endl;
    std::cout << "GLIBCXX version: " << __GLIBCXX__ << std::endl;
	return 0;
}