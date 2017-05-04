$API_URL = "https://api.telegram.org/bot78180438:AAHm7k9cCtUWgdrLSBUm4Cr0QoOn9xhA2R0/"
$ClientID = "e0d93224531208c" #Client ID from imgur
$imgurURL = "https://api.imgur.com/3/"
$lastupdateid = 0

while($true -eq $true){
    $updates = (Invoke-RestMethod -Uri ($API_URL + "getUpdates?offset=" + $lastupdateid + "&timeout=60"))

    for ($i=0; $i -lt $updates.result.count; $i++)
    {
        if($updates.result.message[$i].text -ne $NULL -and $updates.result.message[$i].text.StartsWith("/")) {
                #write-host $updates.result.message[$i].from.first_name
                switch -wildcard ($updates.result.message[$i].text) {        
                    "/random *" {
                        $query = $updates.result.message[$i].text.Substring(8)
                        $querystring = ($query | %{ [Web.HttpUtility]::UrlEncode($_)})   
                        $responses = Invoke-RestMethod -Uri ($imgurURL + "gallery/r/" + $querystring) -Headers @{"Authorization" = "Client-ID $ClientID"}
                        write-host $responses " / " $responses.data.count
                        if($responses.success) {
                            if($responses.data.count -eq 0) {
                                Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=There's either no subreddit named " + $query + " or nothing in imgur for it.")
                            }
                            elseif($responses.data.count -eq 1) {
                                Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=" + $responses.data.link)
                            }
                            else{
                                $random = Get-Random -minimum 0 -maximum $responses.data.count
                                Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=" + $responses.data.link[$random])
                            }
                        }
                        else {
                            Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=Error. HTTP Status " + $responses.status + ". Error: " + $responses.data.error )
                        }
                    }
                    "/search *" {
                        $query = $updates.result.message[$i].text.Substring(8)
                        $querystring = ($query | %{ [Web.HttpUtility]::UrlEncode($_)})   
                        $responses = Invoke-RestMethod -Uri ($imgurURL + "gallery/search/?q=" + $querystring) -Headers @{"Authorization" = "Client-ID $ClientID"}
                        write-host $responses "/" $responses.data.count
                        if($responses.success) {
                            if ($responses.data.count -eq 0) {
                                Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=Sorry bro, there were no results for `"" + $query + "`"")
                            }
                            elseif($responses.data.count -eq 1) {
                                Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=" + $responses.data.link)
                            }
                            else {
                                $random = Get-Random -minimum 0 -maximum ($responses.data.count)
                                Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=" + $responses.data.link[$random])
                            }
                        }
                        else {
                            Invoke-RestMethod -Method Post -Uri ($API_URL + "sendMessage?chat_id=" + $updates.result.message[$i].chat.id + "&text=Error. HTTP Status " + $responses.status + ". Error: " + $responses.data.error )
                        }
                    }

                }
        }
    
        $lastupdateid = $updates.result.update_id[$i] + 1
    }
    start-sleep -s 1
}