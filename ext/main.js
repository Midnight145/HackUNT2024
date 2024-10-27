browser.contextMenus.create({
  id: "search-review",
  title: "Search Reviews for '%s'",
  contexts: ["selection"],
});

browser.contextMenus.onClicked.addListener((info, tab) => {
	if (info.menuItemId === "search-review") {
	    browser.tabs.create({ url: `http://localhost:6068/${encodeURIComponent(info.selectionText)}` });
	}
});

