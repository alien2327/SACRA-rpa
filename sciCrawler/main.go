package main

import (
	"encoding/csv"
	"fmt"
	"goquery"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	"golang.org/x/text/encoding/japanese"
	"golang.org/x/text/transform"
)

type backupcontents struct {
	address     string
	explanation string
}

var scijpurl string = "http://www.sci.kyoto-u.ac.jp/ja/sitemap.html"
var scienurl string = "http://www.sci.kyoto-u.ac.jp/en/sitemap.html"
var baseurl string = "http://www.sci.kyoto-u.ac.jp/"

func main() {
	fmt.Println("Kyoto University Website Backup Script by LYH.")
	datasjp := backup(scijpurl)
	writeJobs(datasjp, "ja")

	datasen := backup(scienurl)
	writeJobs(datasen, "en")

	fmt.Println("Done, extracted japanese web page in length", len(datasjp))
	fmt.Println("Done, extracted english web page in length", len(datasen))
}

func backup(url string) []backupcontents {
	var datas []backupcontents
	fmt.Println("Start connecting " + url)
	res, err := http.Get(url)
	checkERR(err)
	checkCODE(res)

	defer res.Body.Close()

	doc, err := goquery.NewDocumentFromReader(res.Body)
	checkERR(err)

	fmt.Println("Start collecting data...")
	doc.Find(".sitemapHead>a").Each(func(i int, d *goquery.Selection) {
		data := extracter(d)
		datas = append(datas, data)
	})

	return datas

}

func extracter(d *goquery.Selection) backupcontents {
	address, _ := d.Attr("href")
	explanation := cleanString(d.Text())
	return backupcontents{address: address, explanation: explanation}
}

func writeJobs(datas []backupcontents, name string) {
	file, err := os.Create(fmt.Sprintf("backup_%s.csv", name))
	checkERR(err)

	w := csv.NewWriter(file)
	defer w.Flush()

	headers := []string{"Address", "Explanation"}

	wErr := w.Write(headers)
	checkERR(wErr)

	for _, data := range datas {
		japanese, err := utf8tosjis(data.explanation)
		checkERR(err)
		jobSlice := []string{baseurl + fmt.Sprintf("%s/", name) + data.address, japanese}
		fmt.Printf("Writing line in csv, %s\n", jobSlice)
		jwErr := w.Write(jobSlice)
		checkERR(jwErr)
	}
}

func utf8tosjis(str string) (string, error) {
	iostr := strings.NewReader(str)
	rio := transform.NewReader(iostr, japanese.ShiftJIS.NewEncoder())
	ret, err := ioutil.ReadAll(rio)
	if err != nil {
		return "", err
	}
	return string(ret), err
}

func cleanString(str string) string {
	return strings.Join(strings.Fields(strings.TrimSpace(str)), " ")
}

func checkERR(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}

func checkCODE(res *http.Response) {
	if res.StatusCode != 200 {
		log.Fatalln(res.StatusCode)
	}
}
