browser.contextMenus.create({
  id: "search-review",
  title: "Search Reviews for '%s'",
  contexts: ["selection"],
});

browser.contextMenus.onClicked.addListener((info, tab) => {
	if (info.menuItemId === "search-review") {
        const args = { search_str: info.selectionText };
        browser.browserAction.openPopup();
        console.log("Sending message")
        setTimeout(() => {
            browser.runtime.sendMessage({ args: args });
        }, 100);
        console.log("Sent message")
    }
});

