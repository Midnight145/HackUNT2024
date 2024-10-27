browser.contextMenus.create({
  id: "search-review",
  title: "Search Reviews for '%s'",
  contexts: ["selection"],
});

browser.contextMenus.onClicked.addListener((info, tab) => {
	if (info.menuItemId === "search-review") {
        browser.browserAction.openPopup();

        // We run into a race condition here, where the popup is not yet loaded
        // This sucks, but I don't know how to fix it, so I just added a timeout :D
        setTimeout(() => {
            browser.runtime.sendMessage({ search_str: info.selectionText });
        }, 100);
    }
});

