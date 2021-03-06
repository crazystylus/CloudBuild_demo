package main

// Copyright (C) 2021  Kartik Sharma

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	fmt.Println("Starting gin server")
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	counter := 0
	router.GET("/", func(c *gin.Context) {
		counter = counter + 1
		c.Writer.WriteHeader(http.StatusOK)
		c.Writer.Write([]byte(fmt.Sprintf("<html>\n<h2>Hello %s, this website has been visited %d many times</h2>", c.ClientIP(), counter)))
	})
	router.Run("0.0.0.0:8080")
}
