/**
 * @author Jye Tremlett 22613744
 * Created 11/5/2019
 *
 */

import java.util.LinkedList;
import java.util.HashMap;
import java.util.Queue;
import java.util.Arrays;
import java.util.BitSet;



public class MyCITS2200Project implements CITS2200Project {

	HashMap<Integer,LinkedList<Integer>> g;
	HashMap<Integer,LinkedList<Integer>> transpose_g;
	HashMap<String,Integer> urls;
	HashMap<Integer, String> url_inds;
	int num_vertices;


	public MyCITS2200Project() {
		g = new HashMap<>();
		transpose_g = new HashMap<>();
		urls = new HashMap<>();
		url_inds = new HashMap<>();
		num_vertices = 0;
	}

	/**
	 * Adds an edge to the Wikipedia page graph. If the pages do not already exist 
	 * in the graph, they will be added to the graph. g.newEdge checks if the edge 
	 * exists, as we can have two urls in the map urls, without an edge existing
	 * 
	 * @param urlFrom the URL which has a link to urlTo.
	 * @param urlTo the URL which urlFrom has a link to.
	 */
	public void addEdge(String urlFrom, String urlTo) {
		if(!urls.containsKey(urlFrom)) {	//upate urls map if absent
			urls.put(urlFrom, num_vertices);
			url_inds.put(num_vertices, urlFrom);
			num_vertices++;
		}
		if(!urls.containsKey(urlTo)) {		//upate urls map if absent
			urls.put(urlTo, num_vertices);	
			url_inds.put(num_vertices, urlTo);
			num_vertices++;
		}		
		int start = urls.get(urlFrom);
		int end = urls.get(urlTo);	
		
		//add edges for the graph
		if(g.containsKey(start)) {
			g.get(start).add(end);
		}
		else {
			LinkedList<Integer> list = new LinkedList<>();
			list.add(end);
			g.put(start, list);
		}
		if(!g.containsKey(end)) {
			LinkedList<Integer> list = new LinkedList<>();
			g.put(end, list);
		}

		//add edges for our transpose graph
		if(transpose_g.containsKey(end)) {
			transpose_g.get(end).add(start);
		}
		else {
			LinkedList<Integer> list = new LinkedList<>();
			list.add(start);	
			transpose_g.put(end, list);
		}
		if(!transpose_g.containsKey(start)) {
			LinkedList<Integer> list = new LinkedList<>();
			g.put(start, list);
		}
	}


	/**
	 * Finds the shortest path in number of links between two pages.
	 * If there is no path, returns -1.
	 * If seen > -1, the vertex has been visited, and it's value is it's parent
	 * 
	 * @param urlFrom the URL where the path should start.
	 * @param urlTo the URL where the path should end.
	 * @return the length of the shortest path in number of links followed.
	 */
	public int getShortestPath(String urlFrom, String urlTo) {
		if(!urls.containsKey(urlFrom) || !urls.containsKey(urlTo)) {
			return(-1);
		}
		int from = urls.get(urlFrom);
		int to = urls.get(urlTo);
		int[] dists = BFS(from);
		int i = 0;
		System.out.println("to = " + to);
		for(int x:dists) {
			System.out.println("dist from " + from + " to " + i + " = " + x);
			i++;
		}
		return dists[to];
	}

	/**
	 * Method used by getShortestPath and getCentres to find the shortest paths from a specified vertex
	 * @param the vertrex to retrive shortest paths from
	 * @return an array of shortest paths, where index corresponds to the end of the shortest path
	 */
	public int[] BFS(int start) {
		int[] dists = new int[num_vertices];
		int[] seen = new int[num_vertices];
		Arrays.fill(dists, 0);
		Arrays.fill(seen, -1);
		Queue<Integer> S = new LinkedList<Integer>();

		int u = start;			
		S.add(u);
		//Breadth-First Search:
		while(!S.isEmpty()) {
			int v = S.remove();
			LinkedList<Integer> adj = g.get(v);
			if(adj == null) {continue;}
			for(int i:adj) {
				if(seen[i] == -1) {
					dists[i] = dists[v]+1;
					seen[i] = v;
					S.add(i);
				}
			}
		}
		return dists;
	}

	/**
	 * Finds all the centres of the page graph. The order of pages
	 * in the output does not matter. Any order is correct as long as
	 * all the centres are in the array, and no pages that aren't centres
	 * are in the array.
	 * 
	 * @return an array containing all the URLs that correspond to pages that are centers.
	 */
	public String[] getCenters() {
		int[] maxofminpaths = new int[num_vertices];
		int centre = 0;
		int numcentres = 1;
		for(int i = 0; i < num_vertices; i++) {
			int[] dists = BFS(i);
			int max = 0;
			for(int j:dists) {	//if the eccentricity of a path is > the previously stored value, overwrite it:
				if(max <= j) {max = j;}
			}
			maxofminpaths[i] = max;
			if(max == centre) {numcentres++;} //keep track of the current centre(s) and number of centres
			if(max < centre) {
				centre = max;
				numcentres = 1;
			}
			//System.out.println("centre = " + centre + " and numcentres = " + numcentres);
		}
		String[] centres = new String[numcentres];
		int ind = 0;
		int i = 0;
		while(ind < numcentres && i < num_vertices) {
			if(maxofminpaths[i] == centre) {
				centres[ind] = url_inds.get(i);//maybe wrong about i in .get()
				ind++;
			}
			i++;
		}
		return centres;
	}



	/**
	 * Finds all the strongly connected components of the page graph.
	 * Every strongly connected component can be represented as an array 
	 * containing the page URLs in the component. The return value is thus an array
	 * of strongly connected components. The order of elements in these arrays
	 * does not matter. Any output that contains all the strongly connected
	 * components is considered correct.
	 * 
	 * @return an array containing every strongly connected component.
	 */
	public String[][] getStronglyConnectedComponents() {
		BitSet visited = new BitSet(num_vertices);
		LinkedList<String> order = new LinkedList<>();

		int v = 0;
		while(order.size() < num_vertices && v < order.size()) {
			order = DFS(g, visited, order, v);
			v += order.size();
		}

		LinkedList<LinkedList<String>> SCCs = new LinkedList<>();
		v = 0;
		while(SCCs.size() < num_vertices && v < order.size()) {
			if(order.contains(v)) {
				LinkedList<String> scc = DFS(g, visited, order, v);
				SCCs.add(scc);
				v += scc.size();
			}
		}

		String[][] SCC_urls = new String[SCCs.size()][num_vertices];
		for(int p = 0; p < SCCs.size(); p++) {
			//SCC_urls[p][1] = SCCs.pop();
			//for(int c:scc) {
			//	SCC_urls[]
			//}
		}
		return SCC_urls;
	}

	public LinkedList<String> DFS(HashMap<Integer,LinkedList<Integer>> graph, BitSet visited, LinkedList<String> order, int v) {
		visited.set(v);
		for(int next : graph.get(v)) {
			if(!visited.get(next)) { DFS(graph, visited, order, next); }
		}
		order.add(url_inds.get(v));
		return(order);
	}






	/**
	 * Finds a Hamiltonian path in the page graph. There may be many
	 * possible Hamiltonian paths. Any of these paths is a correct output.
	 * This method should never be called on a graph with more than 20
	 * vertices. If there is no Hamiltonian path, this method will
	 * return an empty array. The output array should contain the URLs of pages
	 * in a Hamiltonian path. The order matters, as the elements of the
	 * array represent this path in sequence. So the element [0] is the start
	 * of the path, and [1] is the next page, and so on.
	 * 
	 * @return a Hamiltonian path of the page graph.
	 */
	public String[] getHamiltonianPath() {
		int[] nodepath = new int[num_vertices];
		Arrays.fill(nodepath, -1);
		BitSet visited = new BitSet(num_vertices);						   
		visited.set(0, num_vertices);	//make all visited 1 for base state
		System.out.println("initial visited = " + visited.toString());

		int end = 0;
		while(nodepath[num_vertices-1] == -1 && end < num_vertices) {
			nodepath = checkFromEnd(visited, end,  nodepath);	
			end++;
			//nodepath could be ordered backwards (check)
		}

		String[] path = new String[num_vertices];
		if(nodepath[num_vertices-1] == -1) {return path;}
		for(int i = 0; i<num_vertices; i++) {
			path[i] = url_inds.get(nodepath[i]);
		}
		return path;
	}


	public int[] checkFromEnd(BitSet visited, int end, int[] nodepath) {
		if(!visited.isEmpty() && g.containsKey(end)) {
			visited.clear(end);
			for(int i = visited.nextSetBit(0); i >= 0; i = visited.nextSetBit(i+1)) {
				LinkedList<Integer> adj = g.get(i);
				if(adj.size()>0 && adj.contains(end)) {
					nodepath[visited.cardinality()] = end;//change to num_vertices-visited.cardinality() if nodepath is backwards
					checkFromEnd(visited, i, nodepath);
				}
			}
		}
		//nodepath[visited.size()] = end;
		//this should work, but could try having above in the return statement 
		return(nodepath);
	}
}