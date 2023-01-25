# include <iostream>
# include "curl/curl.h"
using namespace std;

int main(int argc, char* argv[]) {
	CURL* curl;
	CURLcode response;
	curl = curl_easy_init();
	curl_easy_setopt(curl, CURLOPT_URL, argv[1]);

	response = curl_easy_perform(curl);

	cout << response << endl;
	
	curl_easy_cleanup(curl);

	return 0;
}